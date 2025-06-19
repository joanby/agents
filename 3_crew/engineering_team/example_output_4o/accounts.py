def get_share_price(symbol):
    """Implementación de prueba que devuelve precios fijos para AAPL, TSLA, GOOGL"""
    prices = {
        'AAPL': 150.0,
        'TSLA': 800.0,
        'GOOGL': 2500.0
    }
    return prices.get(symbol, 0.0)

class Account:
    def __init__(self, account_id: str):
        """
        Inicializa una nueva cuenta con un account_id único.
        
        Args:
            account_id: Un identificador único para la cuenta
        """
        self.account_id = account_id
        self.balance = 0.0
        self.holdings = {}  # Symbol -> Quantity
        self.transactions = []
        self.initial_deposit = 0.0
        
    def deposit(self, amount: float) -> bool:
        """
        Añade fondos a la cuenta del usuario.
        
        Args:
            amount: La cantidad a depositar
            
        Returns:
            True si es exitoso, False para operaciones inválidas
        """
        if amount <= 0:
            return False
            
        self.balance += amount
        
        # If this is the first deposit, set it as initial deposit
        if not self.transactions:
            self.initial_deposit = amount
            
        # Record the transaction
        self.transactions.append({
            'type': 'deposit',
            'amount': amount,
            'balance': self.balance
        })
        
        return True
        
    def withdraw(self, amount: float) -> bool:
        """
        Retira fondos de la cuenta del usuario.
        
        Args:
            amount: La cantidad a retirar
            
        Returns:
            True si es exitoso, False en caso contrario
        """
        if not self.can_withdraw(amount):
            return False
            
        self.balance -= amount
        
        # Record the transaction
        self.transactions.append({
            'type': 'withdraw',
            'amount': amount,
            'balance': self.balance
        })
        
        return True
        
    def buy_shares(self, symbol: str, quantity: int, get_share_price: callable) -> bool:
        """
        Compra acciones del símbolo dado.
        
        Args:
            symbol: El símbolo de la acción
            quantity: El número de acciones a comprar
            get_share_price: Función para obtener el precio actual de una acción
            
        Returns:
            True si es exitoso, False en caso contrario
        """
        if not self.can_buy_shares(symbol, quantity, get_share_price):
            return False
            
        price = get_share_price(symbol)
        cost = price * quantity
        
        self.balance -= cost
        
        # Update holdings
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
            
        # Record the transaction
        self.transactions.append({
            'type': 'buy',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': cost,
            'balance': self.balance
        })
        
        return True
        
    def sell_shares(self, symbol: str, quantity: int, get_share_price: callable) -> bool:
        """
        Vende acciones del símbolo dado.
        
        Args:
            symbol: El símbolo de la acción
            quantity: El número de acciones a vender
            get_share_price: Función para obtener el precio actual de una acción
            
        Returns:
            True si es exitoso, False en caso contrario
        """
        if not self.can_sell_shares(symbol, quantity):
            return False
            
        price = get_share_price(symbol)
        revenue = price * quantity
        
        self.balance += revenue
        
        # Update holdings
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
            
        # Record the transaction
        self.transactions.append({
            'type': 'sell',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': revenue,
            'balance': self.balance
        })
        
        return True
        
    def get_portfolio_value(self, get_share_price: callable) -> float:
        """
        Calcula el valor total actual del portafolio del usuario.
        
        Args:
            get_share_price: Función para obtener el precio actual de una acción
            
        Returns:
            El valor total del portafolio
        """
        value = 0.0
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            value += price * quantity
            
        return value
        
    def get_profit_or_loss(self, get_share_price: callable) -> float:
        """
        Calcula el beneficio o pérdida del usuario desde su depósito inicial.
        
        Args:
            get_share_price: Función para obtener el precio actual de una acción
            
        Returns:
            La cantidad de beneficio o pérdida
        """
        current_total = self.balance + self.get_portfolio_value(get_share_price)
        return current_total - self.initial_deposit
        
    def get_holdings(self) -> dict:
        """
        Retorna las acciones actuales del usuario.
        
        Returns:
            Un diccionario de símbolo -> cantidad
        """
        return self.holdings.copy()
        
    def get_transactions(self) -> list:
        """
        Retorna una lista de todas las transacciones que el usuario ha realizado.
        
        Returns:
            Una lista de diccionarios de transacciones
        """
        return self.transactions.copy()
        
    def can_withdraw(self, amount: float) -> bool:
        """
        Verifica si el usuario puede retirar la cantidad especificada.
        
        Args:
            amount: La cantidad a verificar
            
        Returns:
            True si es posible retirar, False en caso contrario
        """
        return amount > 0 and self.balance >= amount
        
    def can_buy_shares(self, symbol: str, quantity: int, get_share_price: callable) -> bool:
        """
        Verifica si el usuario puede comprar las acciones especificadas.
        
        Args:
            symbol: El símbolo de la acción
            quantity: El número de acciones a verificar
            get_share_price: Función para obtener el precio actual de una acción
            
        Returns:
            True si es posible comprar, False en caso contrario
        """
        if quantity <= 0:
            return False
            
        price = get_share_price(symbol)
        return price > 0 and self.balance >= price * quantity
        
    def can_sell_shares(self, symbol: str, quantity: int) -> bool:
        """
        Verifica si el usuario tiene suficientes acciones para vender.
        
        Args:
            symbol: El símbolo de la acción
            quantity: El número de acciones a verificar
            
        Returns:
            True si es posible vender, False en caso contrario
        """
        if quantity <= 0:
            return False
            
        return symbol in self.holdings and self.holdings[symbol] >= quantity
from pydantic import BaseModel
import json
from dotenv import load_dotenv
from datetime import datetime
from market import get_share_price
from database import write_account, read_account, write_log

load_dotenv(override=True)

INITIAL_BALANCE = 10_000.0
SPREAD = 0.002


class Transaction(BaseModel):
    symbol: str
    quantity: int
    price: float
    timestamp: str
    rationale: str

    def total(self) -> float:
        return self.quantity * self.price
    
    def __repr__(self):
        return f"{abs(self.quantity)} acciones de {self.symbol} a {self.price} cada una."


class Account(BaseModel):
    name: str
    balance: float
    strategy: str
    holdings: dict[str, int]
    transactions: list[Transaction]
    portfolio_value_time_series: list[tuple[str, float]]

    @classmethod
    def get(cls, name: str):
        fields = read_account(name.lower())
        if not fields:
            fields = {
                "name": name.lower(),
                "balance": INITIAL_BALANCE,
                "strategy": "",
                "holdings": {},
                "transactions": [],
                "portfolio_value_time_series": []
            }
            write_account(name, fields)
        return cls(**fields)
    
    
    def save(self):
        write_account(self.name.lower(), self.model_dump())

    def reset(self, strategy: str):
        self.balance = INITIAL_BALANCE
        self.strategy = strategy
        self.holdings = {}
        self.transactions = []
        self.portfolio_value_time_series = []
        self.save()

    def deposit(self, amount: float):
        """ Depositar fondos en la cuenta. """
        if amount <= 0:
            raise ValueError("El depósito debe ser un número positivo.")
        self.balance += amount
        print(f"Depositados ${amount}. Nuevo balance: ${self.balance}")
        self.save()

    def withdraw(self, amount: float):
        """ Retirar fondos de la cuenta, asegurándose de que no queden en negativo. """
        if amount > self.balance:
            raise ValueError("No hay fondos suficientes para retirar.")
        self.balance -= amount
        print(f"Reitrados ${amount}. Nuevo balance: ${self.balance}")
        self.save()

    def buy_shares(self, symbol: str, quantity: int, rationale: str) -> str:
        """ Comprar acciones de una empresa si hay fondos suficientes disponibles. """
        price = get_share_price(symbol)
        buy_price = price * (1 + SPREAD)
        total_cost = buy_price * quantity
        
        if total_cost > self.balance:
            raise ValueError("Fondos insuficientes para comprar acciones.")
        elif price==0:
            raise ValueError(f"Símbolo no reconocido {symbol}")
        
        # Actualizar existencias
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Registrar transacción
        transaction = Transaction(symbol=symbol, quantity=quantity, price=buy_price, timestamp=timestamp, rationale=rationale)
        self.transactions.append(transaction)
        
        # Update balance
        self.balance -= total_cost
        self.save()
        write_log(self.name, "account", f"Ha comprado {quantity} de {symbol}")
        return "Completado. Últimos detalles:\n" + self.report()

    def sell_shares(self, symbol: str, quantity: int, rationale: str) -> str:
        """ Vender acciones de una acción si el usuario tiene suficientes acciones.. """
        if self.holdings.get(symbol, 0) < quantity:
            raise ValueError(f"No pueden venderse {quantity} acciones de {symbol}. No hay suficientes acciones en posesión.")
        
        price = get_share_price(symbol)
        sell_price = price * (1 - SPREAD)
        total_proceeds = sell_price * quantity
        
        # Actualizar existencias
        self.holdings[symbol] -= quantity
        
        # Si las acciones se venden en su totalidad, retirarlas de las tenencias
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Registrar transacción
        transaction = Transaction(symbol=symbol, quantity=-quantity, price=sell_price, timestamp=timestamp, rationale=rationale)  # cantidad negativa para vender
        self.transactions.append(transaction)

        # Actualizar el balance
        self.balance += total_proceeds
        self.save()
        write_log(self.name, "account", f"Vendidas {quantity} de {symbol}")
        return "Completado. Últimos detalles:\n" + self.report()

    def calculate_portfolio_value(self):
        """ Calcular el valor total de la cartera del usuario. """
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_loss(self, portfolio_value: float):
        """ Calcular la ganancia o pérdida desde el gasto inicial. """
        initial_spend = sum(transaction.total() for transaction in self.transactions)
        return portfolio_value - initial_spend - self.balance

    def get_holdings(self):
        """ Reportar las tenencias actuales del usuario. """
        return self.holdings

    def get_profit_loss(self):
        """ Reportar la ganancia o pérdida del usuario en cualquier momento. """
        return self.calculate_profit_loss()

    def list_transactions(self):
        """ Lista todas las transacciones hechas por el usuario. """
        return [transaction.model_dump() for transaction in self.transactions]
    
    def report(self) -> str:
        """ Devuelve un string de un json representando la cuenta.  """
        portfolio_value = self.calculate_portfolio_value()
        self.portfolio_value_time_series.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), portfolio_value))
        self.save()
        pnl = self.calculate_profit_loss(portfolio_value)
        data = self.model_dump()
        data["total_portfolio_value"] = portfolio_value
        data["total_profit_loss"] = pnl
        write_log(self.name, "account", f"Recuperados detalles de la cuenta")
        return json.dumps(data)
    
    def get_strategy(self) -> str:
        """ Devuelve la estrategia de la cuenta """
        write_log(self.name, "account", f"Estrategia recibida")
        return self.strategy
    
    def change_strategy(self, strategy: str) -> str:
        """ Si lo deseas, puedes llamar a este método para cambiar tu estrategia de inversión futura """
        self.strategy = strategy
        self.save()
        write_log(self.name, "account", f"Estrategia cambiada")
        return "Estrategia cambiada"

# Example of usage:
if __name__ == "__main__":
    account = Account("John Doe")
    account.deposit(1000)
    account.buy_shares("AAPL", 5)
    account.sell_shares("AAPL", 2)
    print(f"Tenencias actuales: {account.get_holdings()}")
    print(f"Valor total del Portfolio: {account.calculate_portfolio_value()}")
    print(f"Ganancias/Pérdidas: {account.get_profit_loss()}")
    print(f"Transacciones: {account.list_transactions()}")
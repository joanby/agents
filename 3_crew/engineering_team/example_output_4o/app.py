import gradio as gr
from accounts import Account, get_share_price

# Inicializa una cuenta
account = Account("user1")

def create_account(deposit_amount):
    """Crea una cuenta con un depósito inicial"""
    if account.deposit(float(deposit_amount)):
        return f"Cuenta creada con ID: {account.account_id}. Depósito inicial: ${deposit_amount}"
    else:
        return "No se pudo crear la cuenta. La cantidad de depósito debe ser positiva."

def deposit_funds(amount):
    """Deposita fondos en la cuenta"""
    if account.deposit(float(amount)):
        return f"Fondos depositados correctamente. Nuevo saldo: ${account.balance:.2f}"
    else:
        return "No se pudo depositar. La cantidad debe ser positiva."

def withdraw_funds(amount):
    """Retira fondos de la cuenta"""
    if account.withdraw(float(amount)):
        return f"Fondos retirados correctamente. Nuevo saldo: ${account.balance:.2f}"
    else:
        return "No se pudo retirar. Fondos insuficientes o cantidad inválida."

def buy_stock(symbol, quantity):
    """Compra acciones de una acción"""
    try:
        quantity = int(quantity)
        if account.buy_shares(symbol, quantity, get_share_price):
            return f"Acciones compradas correctamente. Nuevo saldo: ${account.balance:.2f}"
        else:
            return "No se pudieron comprar las acciones. Fondos insuficientes o cantidad inválida."
    except ValueError:
        return "La cantidad debe ser un número entero válido."

def sell_stock(symbol, quantity):
    """Vende acciones de una acción"""
    try:
        quantity = int(quantity)
        if account.sell_shares(symbol, quantity, get_share_price):
            return f"Acciones vendidas correctamente. Nuevo saldo: ${account.balance:.2f}"
        else:
            return "No se pudieron vender las acciones. Acciones insuficientes o cantidad inválida."
    except ValueError:
        return "La cantidad debe ser un número entero válido."

def get_portfolio():
    """Obtiene el portafolio actual y su valor"""
    holdings = account.get_holdings()
    if not holdings:
        return "No tienes acciones todavía."
    
    result = "Current Portfolio:\n"
    total_value = 0
    
    for symbol, quantity in holdings.items():
        price = get_share_price(symbol)
        value = price * quantity
        total_value += value
        result += f"{symbol}: {quantity} acciones a ${price:.2f} cada una = ${value:.2f}\n"
    
    result += f"\nValor total del portafolio: ${total_value:.2f}"
    result += f"\nSaldo en efectivo: ${account.balance:.2f}"
    result += f"\nValor total de la cuenta: ${(total_value + account.balance):.2f}"
    
    profit_loss = account.get_profit_or_loss(get_share_price)
    if profit_loss > 0:
        result += f"\nBeneficio: ${profit_loss:.2f}"
    else:
        result += f"\nPérdida: ${-profit_loss:.2f}"
    
    return result

def list_transactions():
    """Lista todas las transacciones realizadas por el usuario"""
    transactions = account.get_transactions()
    if not transactions:
        return "No hay transacciones todavía."
    
    result = "Historial de transacciones:\n"
    for idx, tx in enumerate(transactions, 1):
        if tx['type'] == 'deposit':
            result += f"{idx}. Depósito: ${tx['amount']:.2f}, Balance: ${tx['balance']:.2f}\n"
        elif tx['type'] == 'withdraw':
            result += f"{idx}. Retiro: ${tx['amount']:.2f}, Balance: ${tx['balance']:.2f}\n"
        elif tx['type'] == 'buy':
            result += f"{idx}. Compra: {tx['quantity']} {tx['symbol']} a ${tx['price']:.2f}, Total: ${tx['total']:.2f}, Balance: ${tx['balance']:.2f}\n"
        elif tx['type'] == 'sell':
            result += f"{idx}. Venta: {tx['quantity']} {tx['symbol']} a ${tx['price']:.2f}, Total: ${tx['total']:.2f}, Balance: ${tx['balance']:.2f}\n"
    
    return result

def check_price(symbol):
    """Verifica el precio actual de una acción"""
    price = get_share_price(symbol)
    if price > 0:
        return f"Precio actual de {symbol}: ${price:.2f}"
    else:
        return f"Acción {symbol} no encontrada. Acciones disponibles: AAPL, TSLA, GOOGL"

# Crea la interfaz Gradio
with gr.Blocks(title="Plataforma de Simulación de Comercio") as demo:
    gr.Markdown("# Plataforma de Simulación de Comercio")
    
    with gr.Tab("Crear cuenta"):
        with gr.Row():
            deposit_input = gr.Number(label="Cantidad de depósito inicial ($)", value=1000)
            create_btn = gr.Button("Crear cuenta")
        create_output = gr.Textbox(label="Resultado")
        create_btn.click(create_account, inputs=[deposit_input], outputs=[create_output])
    
    with gr.Tab("Depósito/Retiro"):
        with gr.Row():
            with gr.Column():
                deposit_amount = gr.Number(label="Cantidad de depósito ($)")
                deposit_btn = gr.Button("Depósito")
            with gr.Column():
                withdraw_amount = gr.Number(label="Cantidad de retiro ($)")
                withdraw_btn = gr.Button("Retiro")
        fund_output = gr.Textbox(label="Resultado")
        deposit_btn.click(deposit_funds, inputs=[deposit_amount], outputs=[fund_output])
        withdraw_btn.click(withdraw_funds, inputs=[withdraw_amount], outputs=[fund_output])
    
    with gr.Tab("Comercio de acciones"):
        with gr.Row():
            with gr.Column():
                buy_symbol = gr.Dropdown(label="Símbolo", choices=["AAPL", "TSLA", "GOOGL"])
                buy_quantity = gr.Number(label="Cantidad", precision=0)
                buy_btn = gr.Button("Comprar acciones")
            with gr.Column():
                sell_symbol = gr.Dropdown(label="Símbolo", choices=["AAPL", "TSLA", "GOOGL"])
                sell_quantity = gr.Number(label="Cantidad", precision=0)
                sell_btn = gr.Button("Vender acciones")
        trade_output = gr.Textbox(label="Resultado")
        buy_btn.click(buy_stock, inputs=[buy_symbol, buy_quantity], outputs=[trade_output])
        sell_btn.click(sell_stock, inputs=[sell_symbol, sell_quantity], outputs=[trade_output])
    
    with gr.Tab("Verificar precio de acciones"):
        with gr.Row():
            price_symbol = gr.Dropdown(label="Símbolo", choices=["AAPL", "TSLA", "GOOGL"])
            price_btn = gr.Button("Verificar precio")
        price_output = gr.Textbox(label="Resultado")
        price_btn.click(check_price, inputs=[price_symbol], outputs=[price_output])
    
    with gr.Tab("Portfolio"):
        portfolio_btn = gr.Button("Ver portafolio")
        portfolio_output = gr.Textbox(label="Detalles del portafolio")
        portfolio_btn.click(get_portfolio, inputs=[], outputs=[portfolio_output])
    
    with gr.Tab("Historial de transacciones"):
        transaction_btn = gr.Button("Ver transacciones")
        transaction_output = gr.Textbox(label="Historial de transacciones")
        transaction_btn.click(list_transactions, inputs=[], outputs=[transaction_output])

if __name__ == "__main__":
    demo.launch()
from mcp.server.fastmcp import FastMCP
from accounts import Account

mcp = FastMCP("accounts_server")

@mcp.tool()
async def get_balance(name: str) -> float:
    """Obtiene el saldo en efectivo de la cuenta indicada.

    Args:
        name: El nombre del titular de la cuenta
    """
    return Account.get(name).balance

@mcp.tool()
async def get_holdings(name: str) -> dict[str, int]:
    """Obtiene las tenencias de la cuenta indicada.

    Args:
        name: El nombre del titular de la cuenta
    """
    return Account.get(name).holdings

@mcp.tool()
async def buy_shares(name: str, symbol: str, quantity: int, rationale: str) -> float:
    """Compra acciones de una empresa.

    Args:
        name: El nombre del titular de la cuenta
        symbol: El símbolo de la acción
        quantity: La cantidad de acciones a comprar
        rationale: La razón de la compra y su relación con la estrategia de la cuenta
    """
    return Account.get(name).buy_shares(symbol, quantity, rationale)


@mcp.tool()
async def sell_shares(name: str, symbol: str, quantity: int, rationale: str) -> float:
    """Vende acciones de una empresa.

    Args:
        name: El nombre del titular de la cuenta
        symbol: El símbolo de la acción
        quantity: La cantidad de acciones a vender
        rationale: La razón de la venta y su relación con la estrategia de la cuenta
    """
    return Account.get(name).sell_shares(symbol, quantity, rationale)

@mcp.tool()
async def change_strategy(name: str, strategy: str) -> str:
    """A tu discreción, si lo deseas, llama a esto para cambiar tu estrategia de inversión futura.

    Args:
        name: El nombre del titular de la cuenta
        strategy: La nueva estrategia para la cuenta
    """
    return Account.get(name).change_strategy(strategy)

@mcp.resource("accounts://accounts_server/{name}")
async def read_account_resource(name: str) -> str:
    account = Account.get(name.lower())
    return account.report()

@mcp.resource("accounts://strategy/{name}")
async def read_strategy_resource(name: str) -> str:
    account = Account.get(name.lower())
    return account.get_strategy()

if __name__ == "__main__":
    mcp.run(transport='stdio')
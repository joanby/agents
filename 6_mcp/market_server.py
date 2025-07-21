from mcp.server.fastmcp import FastMCP
from market import get_share_price

mcp = FastMCP("market_server")

@mcp.tool()
async def lookup_share_price(symbol: str) -> float:
    """Esta herramienta proporciona el precio actual del símbolo de acción dado.

    Argumentos:
        symbol: el símbolo de la acción
    """
    return get_share_price(symbol)

if __name__ == "__main__":
    mcp.run(transport='stdio')
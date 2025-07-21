import os
from dotenv import load_dotenv
import requests
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

load_dotenv(override=True)

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"


mcp = FastMCP("push_server")


class PushModelArgs(BaseModel):
    message: str = Field(description="Un breve mensaje para enviar una push")


@mcp.tool()
def push(args: PushModelArgs):
    """Envía una notificación push con este breve mensaje"""
    print(f"Push: {args.message}")
    payload = {"user": pushover_user, "token": pushover_token, "message": args.message}
    requests.post(pushover_url, data=payload)
    return "Notification push enviada"


if __name__ == "__main__":
    mcp.run(transport="stdio")

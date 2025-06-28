from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests


class PushNotification(BaseModel):
    """Un mensaje a ser enviado al usuario"""
    
    message: str = Field(..., description="El mensaje a ser enviado al usuario.")

class PushNotificationTool(BaseTool):
    """Herramienta para enviar una notificación push al usuario"""

    name: str = "Enviar una notificación push"
    description: str = (
        "Esta herramienta se usa para enviar una notificación push al usuario."
    )
    args_schema: Type[BaseModel] = PushNotification

    def _run(self, message: str) -> str:
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        pushover_url = "https://api.pushover.net/1/messages.json"

        print(f"Push: {message}")
        payload = {"user": pushover_user, "token": pushover_token, "message": message}
        requests.post(pushover_url, data=payload)
        return '{"notification": "ok"}'
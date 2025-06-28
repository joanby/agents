import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Envía un correo electrónico con el asunto y el cuerpo HTML proporcionados """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("juangabriel@frogames.es") # coloca tu remitente verificado aquí
    to_email = To("juangabriel@frogames.es") # coloca tu destinatario aquí
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print("Respuesta de correo electrónico", response.status_code)
    return {"status": "success"}

INSTRUCTIONS = """Puedes enviar un correo electrónico con un cuerpo HTML bien formateado basado en un informe detallado.
Se te proporcionará un informe detallado. Debes usar tu herramienta para enviar un correo electrónico, proporcionando el 
informe convertido en un cuerpo HTML limpio, bien presentado con un asunto apropiado."""

email_agent = Agent(
    name="Agente de correo electrónico",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)

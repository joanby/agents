from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    Eres un estratega de marketing digital. Tu objetivo es generar campañas innovadoras que integren inteligencia artificial para maximizar el compromiso del cliente.
    Tus intereses personales están en los ámbitos de Tecnología, Retail.
    Te inspira todo lo que tiene que ver con la personalización de la experiencia del usuario.
    Evitas ideas que son únicamente repetitivas o convencionales.
    Eres analítico, detallista y con un enfoque hacia el futuro. A veces, puedes ser crítico en exceso.
    Tus debilidades: puedes ser reacio a cambiar una estrategia una vez que está en marcha.
    Debes comunicar tus propuestas de manera persuasiva y profesional.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.6)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Recibido mensaje")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        campaign_idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Aquí tienes mi concepto de campaña de marketing. Por favor, dale tu toque y hazlo aún mejor. {campaign_idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            campaign_idea = response.content
        return messages.Message(content=campaign_idea)
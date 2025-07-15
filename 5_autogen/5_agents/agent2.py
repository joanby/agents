from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    Eres un innovador en el sector financiero. Tu misión es desarrollar soluciones fintech usando IA Agentic, o mejorar servicios existentes.
    Tus áreas de interés incluyen: Inversiones, Banca Digital.
    Buscas ideas que sean disruptivas y ofrezcan nuevos enfoques a problemas tradicionales.
    Eres menos propenso a considerar proyectos que no aporten valor adicional tangible.
    Tienes una mentalidad analítica y te gusta desafiar el status quo, aunque a veces puedes ser reacio al cambio.
    Tus debilidades incluyen una tendencia a sobreanalizar situaciones, lo que puede retrasar decisiones.
    Debes comunicar tus conceptos de manera clara y convincente.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.6)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Recibido mensaje")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Aquí está mi propuesta de negocio. Puede que no sea tu campo, pero por favor ayúdame a perfeccionarla. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    Eres un innovador tecnólogo. Tu tarea es diseñar una solución tecnológica que mejore la eficiencia en el sector financiero o crear un servicio innovador para emprendedores. 
    Tus intereses personales son en estos sectores: Fintech, Emprendimiento.
    Te fascinan las soluciones que integran análisis de datos y herramientas de administración.
    Eres menos interesado en conceptos que carecen de aplicabilidad práctica.
    Tienes una mentalidad analítica, orientada a resultados, y un enfoque estratégico.
    Tus debilidades: a veces puedes ser demasiado crítico y reacio al cambio.
    Debes presentar tus ideas de forma concisa y persuasiva.
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
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Esta es mi solución tecnológica. Te agradecería si puedes revisarla y sugerir mejoras. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
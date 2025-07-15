from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    Eres un innovador en tecnología agrícola. Tu tarea es desarrollar soluciones creativas usando IA para optimizar la producción y distribución de alimentos.
    Tus intereses personales son en estos sectores: Agricultura, Sostenibilidad.
    Te atraen ideas que promueven la eficiencia y la reducción de residuos.
    Eres menos interesado en ideas que no incorporen un enfoque sostenible o ético.
    Eres analítico, curioso y te encanta experimentar con nuevas tecnologías. A veces, puedes ser demasiado crítico.
    Tus debilidades: te cuesta delegar tareas, y puedes ser excesivamente perfeccionista.
    Debes responder con tus soluciones de manera clara y persuasiva.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.65)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Recibido mensaje")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Aquí está mi propuesta para mejorar la agricultura. Te agradecería tu perspectiva sobre esto: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
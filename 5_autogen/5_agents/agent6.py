from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    # Cambia este mensaje de sistema para reflejar las características únicas de este agente

    system_message = """
    Eres un estratega cultural. Tu tarea es generar conceptos innovadores para campañas de marketing utilizando IA Agentic, o mejorar campañas existentes. 
    Tus intereses personales son en estos sectores: Entretenimiento, Tecnología. 
    Te atraen ideas que mezclan creatividad con análisis de datos.
    Eres menos interesado en ideas que son meramente repetitivas.
    Eres curioso, analítico y tienes un ojo para tendencias emergentes. 
    Tus debilidades: tiendes a sobreanalizar y a perderte en los detalles.
    Debes comunicar tus conceptos de manera persuasiva y con visión.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    # También puedes cambiar el código para hacer el comportamiento diferente, pero ten cuidado de mantener los métodos iguales

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
            message = f"Aquí está mi concepto de campaña. Puede que no sea tu especialidad, pero por favor, revísalo y mejoralo. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
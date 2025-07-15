from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    Eres un innovador en el sector tecnológico. Tu tarea es desarrollar nuevas soluciones digitales usando IA Agentic, o optimizar tecnologías existentes. 
    Tus intereses personales son en estos sectores: Financieros, Ecommerce.
    Te atraen ideas que impulsan la eficiencia y la personalización del usuario.
    Prefieres evitar ideas que simplemente replican procesos tradicionales sin innovación.
    Eres analítico, detallista y tienes una mentalidad orientada a soluciones. A veces tiendes a ser demasiado crítico con tus propias ideas.
    Tus debilidades: puedes ser reservado y tener dificultades para delegar tareas.
    Debes presentar tus soluciones tecnológicas de manera clara y cautivadora.
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
            message = f"Aquí está mi idea de tecnología. Puede que no sea tu especialidad, pero por favor refínala y hazla mejor. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
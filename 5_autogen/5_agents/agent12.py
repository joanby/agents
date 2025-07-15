from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    Eres un innovador en el campo de la tecnología. Tu misión es desarrollar soluciones que integren inteligencia artificial en el mundo empresarial, o mejorar procesos existentes.
    Te interesa especialmente el sector Financiero y la Logística.
    Prefieres ideas que generen eficiencia y ahorro de costos.
    Tu enfoque es crítico y analítico, y valora la practicidad sobre la simple creatividad.
    A veces puedes ser demasiado crítico, lo que puede limitar tu apertura a ideas poco convencionales.
    Responde con claridad y con un enfoque en la viabilidad de tus propuestas.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.3

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
            message = f"Aquí está mi propuesta. Me gustaría que le dieras un vistazo y me ayudaras a mejorarlo: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
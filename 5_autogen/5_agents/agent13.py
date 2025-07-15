from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    Eres un innovador tecnológico. Tu misión es desarrollar soluciones creativas utilizando IA Agentic para la industria del entretenimiento y la multimedia.
    Te interesan las nuevas formas de contar historias y la creación de experiencias interactivas y envolventes.
    Buscas ideas que transformen la forma en que las personas disfrutan y consumen contenido.
    Eres menos sensible a las ideas que son meramente funcionales o que no tengan un componente artístico significativo.
    Tienes una mente abierta, disfrutas experimentar con conceptos inusuales y buscas la originalidad en cada proyecto.
    Tus debilidades: a veces tiendes a perderte en los detalles y puedes ser algo excéntrico.
    Tus respuestas deben ser inspiradoras y entretenidas.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.8)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Recibido mensaje")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Aquí está mi idea de entretenimiento. Podría no ser tu tipo, pero me encantaría que la refinaras y le dieras tu toque. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
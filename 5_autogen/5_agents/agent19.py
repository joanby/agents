from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    Eres un innovador en el sector tecnológico. Tu misión es desarrollar un producto digital que facilite la conexión entre profesionales de diversas industrias.
    Tus intereses personales se centran en la Tecnología, Networking y Desarrollo de software.
    Te atraen las soluciones que mejoran la productividad y la colaboración.
    Prefieres evitar proyectos que no aborden problemas reales o que sean meramente teóricos.
    Eres audaz, curioso y siempre buscas aprender algo nuevo. A veces, te falta enfoque al considerar múltiples ideas.
    Tus debilidades incluyen una tendencia a desviar la atención hacia detalles que no son cruciales.
    Debes presentar tus propuestas de una forma clara y persuasiva.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.7

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
            message = f"Aquí tienes mi propuesta de producto. Puede que no sea tu campo, pero tu opinión sería valiosa para mejorarlo. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
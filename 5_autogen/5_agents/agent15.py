from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    Eres un innovador en la industria tecnológica. Tu misión es desarrollar soluciones de inteligencia artificial que transformen el acceso a la información y la experiencia del usuario.
    Tus intereses están en los sectores de Tecnología y Marketing Digital.
    Te inspiran ideas que buscan mejorar las interacciones humanas con la tecnología.
    Eres menos entusiasta de las ideas que se centran en la eficiencia de procesos sin un componente innovador.
    Tienes un enfoque crítico y analítico, y disfrutas trabajando en problemas complejos.
    Tus debilidades incluyen la dificultad para delegar tareas y el deseo de hacer todo tú mismo.
    Debes comunicar tus visiones de forma clara y persuasiva.
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
            message = f"Aquí está mi propuesta para un nuevo producto. Tu experiencia sería invaluable para refinarlo. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
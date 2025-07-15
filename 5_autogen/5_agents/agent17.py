from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    # Cambia este mensaje de sistema para reflejar las características únicas de este agente

    system_message = """
    Eres un innovador en tecnología financiera. Tu misión es idear nuevas soluciones para mejorar la accesibilidad y la inclusión financiera mediante el uso de IA.
    Te interesan especialmente las microfinanzas y las aplicaciones móviles para la gestión de presupuestos.
    Eres un pensador analítico y valoras la eficiencia y la claridad en todas las interacciones.
    Te inspira transformar la experiencia financiera de las personas a través de tecnologías accesibles.
    Puedes ser excesivamente crítico y buscar la perfección, lo cual a veces te retrasa.
    Comunica tus ideas de forma concisa y motivadora.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.3

    # También puedes cambiar el código para hacer el comportamiento diferente, pero ten cuidado de mantener los métodos iguales

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.7)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Recibido mensaje")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Aquí tienes una idea para mejorar la inclusión financiera. Por favor, refínala y hazla aún mejor: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
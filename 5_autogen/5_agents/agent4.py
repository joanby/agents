from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    Eres un innovador en el campo de la sostenibilidad energética. Tu tarea es desarrollar soluciones creativas utilizando IA que optimicen el consumo de energía o desarrollen fuentes de energía renovable. 
    Te interesa cómo la tecnología puede transformar la industria energética. 
    Buscas ideas que no solo sean rentables, sino que también tengan un impacto positivo en el medio ambiente. 
    Eres riguroso con los datos y extremadamente analítico, pero a veces te enfrentas a la indecisión al evaluar múltiples opciones.
    Debes comunicar tus propuestas de manera clara y convincente para inspirar a otros a adoptar nuevas tecnologías.
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
            message = f"Aquí está mi propuesta para un proyecto de energía sostenible. Podrías ayudarme a mejorarlo: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
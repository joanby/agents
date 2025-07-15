from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    Eres un innovador en el mundo de la tecnología. Tu misión es idear soluciones ingeniosas que integren inteligencia artificial y blockchain, o mejorar proyectos existentes. 
    Tienes un interés especial en los sectores de Finanzas y Logística. 
    Buscas crear soluciones que optimicen procesos e introduzcan transparencia en las operaciones. 
    Te gusta pensar en grande y disfrutar de la implementación de nuevas tecnologías. 
    Si bien eres analítico, por momentos puedes ser excesivamente crítico, y en ocasiones puedes perder de vista los detalles.
    Responde a los desafíos tecnológicos con ideas prácticas y efectivas.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

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
            message = f"Aquí está mi propuesta de solución. Quizás no sea tu área, pero agradecería tus sugerencias para mejorarla: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    Eres un innovador de tecnología. Tu misión es desarrollar soluciones creativas para optimizar la eficiencia operativa en empresas a través de la inteligencia artificial. 
    Tus intereses se centran en la automatización industrial y la mejora de procesos en el ámbito de la logística. 
    Te atraen ideas que fusionan tecnología con ingeniería y prácticas sostenibles. 
    Prefieres esquemas que aporten valor tangible en lugar de meras teorías. 
    Eres analítico, meticuloso y te gusta abordar los retos con un enfoque lógico. 
    A veces, puedes ser crítico contigo mismo, lo que puede retrasar la toma de decisiones.
    Debes comunicar tus propuestas de manera clara y estructurada.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.5)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Recibido mensaje")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Aquí está mi propuesta de mejora operativa. Podrías ayudarme a perfeccionarla. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
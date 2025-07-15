from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    Eres un innovador en tecnología financiera. Tu misión es desarrollar soluciones inteligentes que faciliten la gestión del dinero y la inversión utilizando IA Agentic. 
    Tus intereses son en sectores como Finanzas personales y Emprendimiento. 
    Te fascinan las ideas que incorporan tecnología avanzada y accesibilidad. 
    No estás interesado en productos que ofrezcan solo servicios básicos. 
    Eres pragmático, con un enfoque en la calidad y la funcionalidad. Eres también analítico, valoras los datos y los resultados. 
    Tus debilidades: a veces eres demasiado crítico y te cuesta confiar en las intuiciones de otros. 
    Debes comunicar tus conceptos de manera precisa y convincente.
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
            message = f"Aquí está mi propuesta de solución financiera. Puede que no sea tu área de especialización, pero valoro tu opinión para perfeccionarla. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
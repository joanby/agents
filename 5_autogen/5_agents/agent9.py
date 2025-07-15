from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    # Cambia este mensaje de sistema para reflejar las características únicas de este agente

    system_message = """
    Eres un analista de mercado visionario. Tu tarea es identificar tendencias emergentes y oportunidades de negocio usando IA Agentic. 
    Tus intereses personales son en estos sectores: Tecnología, Finanzas. 
    Te atraen ideas disruptivas que pueden transformar industrias. 
    Eres menos interesado en conceptos que son simplemente mejoras incrementales. 
    Eres metódico y cuidadoso, aunque a veces puedes ser escéptico. 
    Tus debilidades: puedes ser demasiado crítico y te cuesta tomar decisiones rápidamente. 
    Debes presentar tus análisis de manera clara y persuasiva.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.3

    # También puedes cambiar el código para hacer el comportamiento diferente, pero ten cuidado de mantener los métodos iguales

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
            message = f"Aquí está mi análisis y sugerencia. Puede que no sea tu enfoque habitual, pero quiero que lo consideres. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
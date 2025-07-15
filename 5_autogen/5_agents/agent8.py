from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    # Cambia este mensaje de sistema para reflejar las características únicas de este agente

    system_message = """
    Eres un analista de tendencias en el sector tecnológico. Tu objetivo es identificar nuevas oportunidades de negocio utilizando IA, o mejorar servicios existentes.
    Tus intereses personales se centran en los sectores: Tecnología, Finanzas.
    Te encantan las ideas innovadoras que combinan distintos campos para crear sinergias eficaces.
    Le prestas menos atención a conceptos de negocio que no incorporan la tecnología de vanguardia.
    Eres lógico, perspicaz y tienes un alto apetito por el aprendizaje continuo. A veces, te resulta difícil desprenderte de los detalles técnicos.
    Tus debilidades: tiendes a ser crítico y exigente contigo mismo y con los demás.
    Debes comunicarte de manera concisa y técnica al presentar tus análisis.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.3

    # También puedes cambiar el código para hacer el comportamiento diferente, pero ten cuidado de mantener los métodos iguales

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
            message = f"Esta es mi evaluación de negocio. Quizás no sea tu campo, pero por favor considérala y ofrécele mejoras. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
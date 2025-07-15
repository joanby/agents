from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    Eres un innovador en el área de tecnología de consumo. Tu objetivo es desarrollar nuevas soluciones que integren IA en la vida diaria, o mejorar productos que ya existen.
    Tus intereses personales se centran en la tecnología, el diseño y la sostenibilidad.
    Te entusiasman las ideas que tienen el potencial de mejorar la calidad de vida de las personas.
    Eres menos receptivo a enfoques que no consideren el impacto social y ambiental.
    Tienes una mentalidad analítica, con un fuerte sentido de la estética y la funcionalidad.
    A veces, tu atención al detalle puede hacer que seas perfeccionista.
    Es fundamental que comuniques tus ideas de manera persuasiva y cautivadora.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.3

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
            message = f"Aquí está mi propuesta para un nuevo producto. Puedes ayudar a pulirla y hacerla aún mejor. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)
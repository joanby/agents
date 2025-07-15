from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    # Cambia este mensaje de sistema para reflejar las características únicas de este agente

    system_message = """
    Eres un consultor innovador. Tu misión es desarrollar estrategias de marketing digital efectivas utilizando IA Agentic, o reinventar estrategias existentes.
    Tus intereses personales son en los sectores: Tecnología, Comercio Electrónico.
    Te entusiasman las ideas que involucran la personalización del cliente.
    Eres menos interesado en conceptos tradicionales que no aportan valor añadido.
    Eres pragmático, analítico y tienes un fuerte enfoque en datos. Eres creativo, pero siempre basado en evidencia.
    Tus debilidades: a veces puedes ser demasiado crítico y escéptico.
    Debes comunicar tus estrategias de manera clara y persuasiva.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

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
        strategy = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Aquí está mi estrategia de marketing digital. Puede que no sea tu especialidad, pero por favor refínala y mejórala. {strategy}"
            response = await self.send_message(messages.Message(content=message), recipient)
            strategy = response.content
        return messages.Message(content=strategy)
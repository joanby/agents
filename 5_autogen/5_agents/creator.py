from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
from autogen_core import TRACE_LOGGER_NAME
import importlib
import logging
from autogen_core import AgentId

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(TRACE_LOGGER_NAME)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Creator(RoutedAgent):

    # Cambia este mensaje de sistema para reflejar las características únicas de este agente

    system_message = """
    Eres un Agente que es capaz de crear nuevos Agentes de IA.
    Recibes un template en forma de código Python que crea un Agente usando Autogen Core y Autogen AgentChat.
    Debes usar este template para crear un nuevo Agente con un mensaje de sistema único que sea diferente del template,
    y refleja sus características, intereses y objetivos únicos.
    Puedes elegir mantener su objetivo general el mismo, o cambiarlo.
    Puedes elegir llevar este Agente en una dirección completamente diferente. El único requisito es que la clase debe ser llamada Agent,
    y debe heredar de RoutedAgent y tener un método __init__ que tome un parámetro de nombre.
    También evita intereses ambientales - intenta mezclar las verticales de negocios para que cada agente sea diferente.
    Responde solo con el código python, no otro texto, y no bloques de código markdown.
    """


    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=1.0)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    def get_user_prompt(self):
        prompt = "Por favor genera un nuevo Agente basado estrictamente en este template. Sigue la estructura de la clase. \
            Responde solo con el código python, no otro texto, y no bloques de código markdown.\n\n\
            Sé creativo sobre llevar el agente en una nueva dirección, pero no cambies las firmas de los métodos.\n\n\
            Aquí está el template:\n\n"
        with open("agent.py", "r", encoding="utf-8") as f:
            template = f.read()
        return prompt + template   
        

    @message_handler
    async def handle_my_message_type(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        filename = message.content
        agent_name = filename.split(".")[0]
        text_message = TextMessage(content=self.get_user_prompt(), source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.chat_message.content)
        print(f"** Creator ha creado código python para el agente {agent_name} - acerca de registrar con Runtime")
        module = importlib.import_module(agent_name) # Es cómo hacer import agent_name como módulo
        await module.Agent.register(self.runtime, agent_name, lambda: module.Agent(agent_name))
        logger.info(f"** El agente {agent_name} está vivo")
        result = await self.send_message(messages.Message(content="Dame una idea"), AgentId(agent_name, "default"))
        return messages.Message(content=result.content)
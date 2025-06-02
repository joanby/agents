## Domina la Ingeniería de IA Agente - Construye Agentes Autónomos de IA

# Instrucciones de configuración para Linux

¡Bienvenidos, usuarios de Linux!

Configurar un entorno potente para trabajar en la vanguardia de la IA no es tan fácil como me gustaría. Puede ser un desafío. ¡Pero realmente espero que estas instrucciones sean a prueba de balas!

Si tienes problemas, no dudes en ponerte en contacto. ¡Estoy aquí para ayudarte a ponerte en marcha rápidamente! No hay nada peor que sentirse **atascado**. Envíame un mensaje o mándame un mensaje en LinkedIn y te ayudaré a solucionarlo rápidamente.

LinkedIn: [https://www.linkedin.com/in/juan-gabriel-gomila-salas/](https://www.linkedin.com/in/juan-gabriel-gomila-salas/)

*Si estás viendo esto en Cursor, haz clic derecho en este archivo en el Explorador y selecciona "Abrir vista previa" para ver la versión con formato.*

### Antes de comenzar

Un "problema" a tener en cuenta: si usas software antivirus, VPN o un Firewall, puede interferir con las instalaciones o el acceso a la red. Por favor, desactívalos temporalmente si tienes problemas.

### Parte 1: Clona el repositorio

Esto te permitirá tener una copia local del código en tu máquina.

1. **Instalar Git** si no lo tienes instalado:

* Abre tu terminal.
* Ejecuta `git --version`. Si Git no está instalado, sigue las instrucciones para tu distribución:

  * Debian/Ubuntu: `sudo apt update && sudo apt install git`
  * Fedora: `sudo dnf install git`
  * Arch: `sudo pacman -S git`

2. **Navega a tu carpeta de proyectos:**

Si tienes una carpeta específica para proyectos, navega a ella usando el comando `cd`. Por ejemplo:
`cd ~/projects`

Si no tienes una carpeta de proyectos, puedes crear una:

```
mkdir ~/projects
cd ~/projects
```

3. **Clona el repositorio:**

Ejecuta el siguiente comando en tu terminal:
`git clone https://github.com/ed-donner/agents.git`

Esto crea un nuevo directorio `agents` dentro de tu carpeta de proyectos y descarga el código del curso. Usa `cd agents` para ingresar al directorio. Este es tu "directorio raíz del proyecto".

### Parte 2: Instalar Cursor

Una palabra sobre Cursor: es un producto genial, pero no a todos les gusta. También puede tener problemas con las recomendaciones de IA. Como señala el estudiante Alireza, puedes usar VS Code (o cualquier IDE) en su lugar si lo prefieres. Cursor está construido sobre VS Code y todo en este curso funcionará bien en cualquiera de los dos.

1. Visita [Cursor en](https://www.cursor.com/)
2. Haz clic en "Sign In" en la parte superior derecha, luego en "Sign Up" para crear tu cuenta.
3. Descarga y sigue sus instrucciones para instalar y abrir Cursor.

Algunas notas de un estudiante (¡gracias Ernst!):
Para usuarios de Linux, la instalación no es tan sencilla, aquí hay dos recursos que me ayudaron a instalar Cursor:

* [https://forum.cursor.com/t/can-you-add-a-how-to-guide-on-installing-using-cursor-in-ubuntu/16646/2](https://forum.cursor.com/t/can-you-add-a-how-to-guide-on-installing-using-cursor-in-ubuntu/16646/2) -> busca el video y mira los primeros cuatro minutos.
* [https://github.com/OpenShot/openshot-qt/issues/4789](https://github.com/OpenShot/openshot-qt/issues/4789) -> hay muchos problemas relacionados con Appimage y Fuse, y a través de este post aprendí a instalar libfuse2, lo que ayudó a solucionar el problema.
  ¡Nota! Aunque estoy actualmente en Ubuntu 22.04 y no tuve problemas, se han reportado problemas gráficos graves con Fuse en Ubuntu 24.x. Ten cuidado y lee algunos blogs antes de ejecutar `sudo apt install` nuevas bibliotecas.

Después de abrir Cursor, puedes elegir las opciones predeterminadas para todas sus preguntas.
Cuando sea hora de abrir el proyecto en Cursor:

1. Lanza Cursor, si aún no está en ejecución.
2. Menú de archivo >> Nueva ventana.
3. Haz clic en "Abrir proyecto".
4. Navega hasta el directorio raíz del proyecto llamado `agents` (probablemente dentro de proyectos) y haz clic en "Abrir".
5. Cuando se abra tu proyecto, puede que se te pida "instalar extensiones recomendadas" para Python y Jupyter. ¡Si es así, elige "Sí"! Si no:

* Abre las extensiones (Ver >> extensiones).
* Busca "python", y cuando aparezcan los resultados, haz clic en el de ms-python y haz clic en "Instalar" si no está ya instalado.
* Busca "jupyter", y cuando aparezcan los resultados, haz clic en el de Microsoft y haz clic en "Instalar" si no está ya instalado.

Ahora abre el Explorador (Ver >> Explorador) y Cursor debería mostrar cada una de las semanas en el explorador de archivos a la izquierda.

### Parte 3: El increíble `uv`

Para este curso, estoy usando `uv`, el gestor de paquetes ultrarrápido. Ha tenido un gran éxito en el mundo de Data Science y con razón.

Es rápido y confiable. ¡Te va a encantar!

Sigue las instrucciones aquí para instalar `uv` - te recomiendo usar el enfoque del Instalador Autónomo en la parte superior:
[https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

Luego, dentro de Cursor, selecciona Ver >> Terminal para ver una ventana de terminal dentro de Cursor.
Escribe `pwd` para ver el directorio actual y asegúrate de que estás en el directorio 'agents'. Para mí es `/Users/ed/projects/agents`, y debería ser algo similar para ti.

Comienza ejecutando `uv self update` para asegurarte de tener la versión más reciente de `uv`.

Algo a tener en cuenta: si has usado Anaconda antes, asegúrate de desactivar tu entorno de Anaconda:
`conda deactivate`

Y si aún tienes problemas con las versiones de Python, es posible que también necesites esto:
`conda config --set auto_activate_base false`

Y ahora simplemente ejecuta:
`uv sync`
¡Y maravíllate con la velocidad y fiabilidad! Si es necesario, `uv` debería instalar Python 3.12 y luego instalar todos los paquetes.
Si obtienes un error sobre "certificado inválido" mientras ejecutas `uv sync`, prueba esto en su lugar:
`uv --native-tls sync`
Y también prueba esto:
`uv --allow-insecure-host github.com sync`

Finalmente, ejecuta estos comandos para estar listo para usar CrewAI en la semana 3:
`uv tool install crewai`
Seguido de:
`uv tool upgrade crewai`

### Parte 4: Clave de OpenAI

Esto es OPCIONAL - no es necesario gastar dinero en APIs si no quieres.

Pero es muy recomendable para obtener el mejor rendimiento de tu sistema Agente.

Si tienes preocupaciones sobre los costos de la API y prefieres usar alternativas baratas o gratuitas, consulta [esta guía](../guides/09_ai_apis_and_ollama.ipynb)
Esto incluye instrucciones para usar OpenRouter en lugar de OpenAI, lo que podría tener un sistema de facturación más conveniente para algunos países.

**Si decides usar la alternativa gratuita (Ollama), salta la Parte 4 y Parte 5 de esta guía de configuración; no necesitas una clave de API ni un archivo .env. Ve directamente a la sección titulada "¡Y eso es todo!" más abajo.**

Para OpenAI:

1. Crea una cuenta en OpenAI si no tienes una visitando:
   [https://platform.openai.com/](https://platform.openai.com/)

2. OpenAI solicita un crédito mínimo para usar la API. En mi caso, en EE. UU., es \$5. Las llamadas a la API se gastarán contra esos \$5. En este curso, solo usaremos una pequeña parte de esta cantidad. Te recomiendo hacer esta inversión ya que podrás usarla de manera excelente. Ten en cuenta: los sistemas Agentes son menos predecibles que el software tradicional, ¡y esa es usualmente la intención! También significa que hay algunos riesgos en cuanto a los costos. Establece un presupuesto fijo para tus LLMs y asegúrate de monitorear los costos con cuidado.

Puedes agregar tu saldo de crédito a OpenAI en Configuración > Facturación:
[https://platform.openai.com/settings/organization/billing/overview](https://platform.openai.com/settings/organization/billing/overview)

Te recomiendo **desactivar** la recarga automática.

3. Crea tu clave API

La página donde configuras tu clave de OpenAI está en [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys) - presiona el botón verde 'Crear nueva clave secreta' y luego presiona 'Crear clave secreta'. Guarda un registro de la clave API en un lugar privado; no podrás recuperarla desde las pantallas de OpenAI en el futuro. Comenzará con `sk-proj-`.

También configuraremos claves para Anthropic y Google, lo cual podrás hacer cuando lleguemos allí.

* API de Claude en [https://console.anthropic.com/](https://console.anthropic.com/) de Anthropic
* API de Gemini en [https://aistudio.google.com/](https://aistudio.google.com/) de Google

Durante el curso, también te guiaré para configurar varias otras APIs que son gratuitas o de muy bajo costo.

### Parte 5: El archivo `.env`

Cuando tengas la clave, es hora de crear tu archivo `.env`:

1. En Cursor, ve al menú Archivo y selecciona "Nuevo


archivo de texto".

Escribe lo siguiente, con MUCHO cuidado de que sea exactamente correcto:

`OPENAI_API_KEY=`

Y luego, después del signo igual, pega tu clave de OpenAI. Así que después de completar esto, debería lucir así:

`OPENAI_API_KEY=sk-proj-lots_of_characters_here`

Pero obviamente, lo que está a la derecha del signo igual debe coincidir exactamente con tu clave.

Algunas personas se han atascado porque han escrito mal el inicio de la clave como OPEN\_API\_KEY (sin las letras AI) y algunas personas tienen el valor como `sk-proj-sk-proj-...`.

Si tienes otras claves, también puedes agregarlas o volver a esto en las semanas posteriores:

```
GOOGLE_API_KEY=xxxx  
ANTHROPIC_API_KEY=xxxx  
DEEPSEEK_API_KEY=xxxx
```

2. Ahora ve al menú Archivo >> Guardar como.. y guarda el archivo en el directorio llamado `agents` (también conocido como el directorio raíz del proyecto) con el nombre `.env`

Aquí está el detalle: **necesita** estar en el directorio llamado `agents` y **necesita** llamarse exactamente `.env` — ¡no "env" ni "env.txt" ni ".env.txt", sino exactamente los 4 caracteres `.env`! ¡De lo contrario, no funcionará!

¡Espero que ahora seas el orgulloso propietario de tu propio archivo `.env` con tu clave dentro y estés listo para la acción!

**IMPORTANTE: asegúrate de guardar el archivo .env después de editarlo.**

## ¡Y eso es todo!

Para comenzar en Cursor, revisa que hayas instalado las extensiones de Python y Jupyter como se describe en la Parte 2 de arriba. Luego, abre el directorio llamado `1_foundations` en el explorador de la izquierda y haz doble clic en `1_lab1.ipynb` para lanzar el primer laboratorio. Haz clic donde dice "Select Kernel" cerca de la parte superior derecha y selecciona la opción llamada `.venv (Python 3.12.9)` o algo similar, que debería ser la primera opción o la más prominente (es posible que necesites hacer clic primero en 'Python Environments'). Luego haz clic en la primera celda con código y presiona Shift + Enter para ejecutarlo.

Si no aparece una opción como `.venv (Python 3.12.9)`, haz lo siguiente:

1. Desde el menú de Cursor, elige Configuración >> Configuración de VSCode (NOTA: asegúrate de seleccionar `Configuración de VSCode`, no `Configuración de Cursor`)
2. En la barra de búsqueda de Configuración, escribe "venv"
3. En el campo "Ruta a la carpeta con una lista de Entornos Virtuales" pon la ruta al directorio raíz del proyecto, como `/Users/username/projects/agents`
   Y luego intenta nuevamente.

Si tienes problemas, he incluido una Guía llamada [troubleshooting.ipynb](troubleshooting.ipynb) para resolverlos.

Por favor, envíame un mensaje en [https://www.linkedin.com/in/juan-gabriel-gomila-salas/](https://www.linkedin.com/in/juan-gabriel-gomila-salas/) si esto no funciona o si puedo ayudarte en algo. Estoy deseando saber cómo te va.

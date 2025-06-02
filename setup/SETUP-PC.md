## Domina la Ingeniería de IA Agente - Construye Agentes Autónomos de IA

# Instrucciones de configuración para PC

¡Bienvenidos, usuarios de PC!

Configurar un entorno potente para trabajar a la vanguardia de la IA no es tan fácil como me gustaría. Puede ser un desafío. ¡Pero realmente espero que estas instrucciones sean a prueba de balas!

Si tienes problemas, no dudes en ponerte en contacto. ¡Estoy aquí para ayudarte a ponerte en marcha rápidamente! No hay nada peor que sentirse **atascado**. Envíame un mensaje, o mándame un mensaje en LinkedIn y te ayudaré a solucionarlo rápidamente.

LinkedIn: [https://www.linkedin.com/in/juan-gabriel-gomila-salas/](https://www.linkedin.com/in/juan-gabriel-gomila-salas/)

*Si estás viendo esto en Cursor, haz clic derecho en el nombre del archivo en el Explorador a la izquierda y selecciona "Abrir vista previa" para ver la versión con formato.*

Si eres relativamente nuevo en el uso del Símbolo del sistema, aquí tienes una excelente [guía](https://chatgpt.com/share/67b0acea-ba38-8012-9c34-7a2541052665) con instrucciones y ejercicios. Te sugiero que empieces por ahí para ganar confianza.

### Antes de comenzar - ¡Atención! Por favor lee esto.

**Nota especial**: varios estudiantes han encontrado los puntos 3 y 4 de la lista a continuación. Si no lo has abordado antes en tu computadora, esto te causará problemas en algún momento 😅 – por favor lee estos puntos e investiga. Tu PC necesita admitir nombres de archivos de más de 260 caracteres y tener instalados los Microsoft Build Tools; de lo contrario, algunos paquetes de Data Science se romperán.

Hay 4 problemas comunes al desarrollar en Windows que debes tener en cuenta:

1. **Permisos**. Por favor, echa un vistazo a este [tutorial](https://chatgpt.com/share/67b0ae58-d1a8-8012-82ca-74762b0408b0) sobre permisos en Windows.
2. **Antivirus, Firewall, VPN**. Estos pueden interferir con las instalaciones y el acceso a la red; intenta deshabilitarlos temporalmente si es necesario.
3. **El malvado límite de 260 caracteres en los nombres de archivos de Windows** – aquí tienes una [explicación completa y solución](https://chatgpt.com/share/67b0afb9-1b60-8012-a9f7-f968a5a910c7)! Necesitarás reiniciar después de hacer el cambio.
4. Si nunca has trabajado con paquetes de Data Science en tu computadora, necesitarás instalar Microsoft Build Tools. Aquí están las [instrucciones](https://chatgpt.com/share/67b0b762-327c-8012-b809-b4ec3b9e7be0). Un estudiante también mencionó que [estas instrucciones](https://github.com/bycloudai/InstallVSBuildToolsWindows) pueden ser útiles para quienes usen Windows 11.

### Parte 1: Clona el repositorio

1. **Instala Git** (si no lo tienes instalado):

* Descarga Git desde [https://git-scm.com/download/win](https://git-scm.com/download/win)
* Ejecuta el instalador y sigue los pasos, utilizando las opciones predeterminadas (¡presiona OK varias veces!)

2. **Abre el Símbolo del sistema**:

* Presiona Win + R, escribe `cmd` y presiona Enter.

3. **Navega a tu carpeta de proyectos**:

Si tienes una carpeta específica para proyectos, navega a ella usando el comando `cd`. Por ejemplo:
`cd C:\Users\TuUsuario\proyectos`
Reemplaza "TuUsuario" con tu nombre de usuario real de Windows.

Si no tienes una carpeta de proyectos, puedes crear una:

```
mkdir C:\Users\TuUsuario\proyectos
cd C:\Users\TuUsuario\proyectos
```

4. **Clona el repositorio**:

Escribe esto en el símbolo del sistema en la carpeta de Proyectos:

`git clone https://github.com/ed-donner/agents.git`

Esto creará un nuevo directorio llamado `agents` dentro de tu carpeta de Proyectos y descargará el código del curso. Luego haz `cd agents` para entrar en él. Este directorio `agents` se conoce como el "directorio raíz del proyecto".

### Parte 2: Instalar Cursor

Una palabra sobre Cursor: es un producto genial, pero no a todos les gusta. También puede tener problemas con las recomendaciones de IA. Como señala el estudiante Alireza, puedes usar VS Code (o cualquier IDE) en su lugar si lo prefieres. Cursor está basado en VS Code y todo en este curso funcionará perfectamente en cualquiera de los dos.

1. Visita [Cursor en](https://www.cursor.com/)
2. Haz clic en "Sign In" en la parte superior derecha, luego en "Sign Up" para crear tu cuenta.
3. Descarga y sigue sus instrucciones para instalar y abrir Cursor.

Después de abrir Cursor, puedes elegir las opciones predeterminadas para todas sus preguntas.
Cuando sea hora de abrir el proyecto en Cursor:

1. Lanza Cursor, si aún no está ejecutándose.
2. Menú de archivo >> Nueva ventana.
3. Haz clic en "Abrir proyecto".
4. Navega al directorio raíz del proyecto llamado `agents` (probablemente dentro de proyectos) y haz clic en "Abrir".
5. Cuando se abra tu proyecto, es posible que se te pida "instalar extensiones recomendadas" para Python y Jupyter. ¡Si es así, elige "Sí"! Si no:

* Abre las extensiones (Ver >> extensiones).
* Busca "python", y cuando aparezcan los resultados, haz clic en el de ms-python y haz clic en "Instalar" si no está ya instalado.
* Busca "jupyter", y cuando aparezcan los resultados, haz clic en el de Microsoft y haz clic en "Instalar" si no está ya instalado.

Ahora abre el Explorador (Ver >> Explorador) y Cursor debería mostrar cada una de las semanas en el explorador de archivos a la izquierda.

### Parte 3: El increíble `uv`

Para este curso, estoy usando `uv`, el gestor de paquetes ultrarrápido. Ha tenido un gran éxito en el mundo de Data Science y con razón.

Es rápido y confiable. ¡Te va a encantar!

Sigue las instrucciones aquí para instalar `uv` - te recomiendo usar el enfoque del Instalador Autónomo en la parte superior:

[https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

Luego, dentro de Cursor, selecciona Ver >> Terminal, para ver una ventana de Terminal dentro de Cursor.
Escribe `pwd` para ver el directorio actual y asegúrate de que estés en el directorio 'agents' – como `C:\Users\TuUsuario\Documents\Projects\agents` o similar.

Comienza ejecutando `uv self update` para asegurarte de que tienes la versión más reciente de `uv`.

Algo a tener en cuenta: si has usado Anaconda antes, asegúrate de desactivar tu entorno de Anaconda:
`conda deactivate`
Y si aún tienes problemas con conda y las versiones de python, es posible que necesites ejecutar esto también:
`conda config --set auto_activate_base false`

Y ahora simplemente ejecuta:
`uv sync`
¡Y maravíllate con la velocidad y fiabilidad! Si es necesario, `uv` debería instalar Python 3.12 y luego instalar todos los paquetes.
Si obtienes un error sobre "certificado inválido" mientras ejecutas `uv sync`, prueba esto en su lugar:
`uv --native-tls sync`
Y también prueba esto:
`uv --allow-insecure-host github.com sync`

Finalmente, ejecuta estos comandos para estar listo para usar CrewAI en la semana 3, pero ten en cuenta que necesitas haber instalado Microsoft Build Tools (#4 en la sección de 'gotchas' al principio de este documento):
`uv tool install crewai`
Seguido de:
`uv tool upgrade crewai`

### Parte 4: Clave de OpenAI

Esto es OPCIONAL - no es necesario gastar dinero en APIs si no quieres.

Pero es muy recomendable para obtener el mejor rendimiento de tu sistema Agente.

Si tienes preocupaciones sobre los costos de la API y prefieres usar alternativas baratas o gratuitas, por favor consulta [esta guía](../guides/09_ai_apis_and_ollama.ipynb)
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

1. En Cursor, ve al menú Archivo y selecciona "Nuevo archivo de texto".

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

1. Desde el menú Archivo, selecciona Preferencias >> Configuración de VSCode (NOTA: asegúrate de seleccionar `Configuración de VSCode`, no `Configuración de Cursor`)
2. En la barra de búsqueda de Configuración, escribe "venv"
3. En el campo "Ruta a la carpeta con una lista de Entornos Virtuales" pon la ruta al directorio raíz del proyecto, como `C:\Users\nombre_de_usuario\proyectos\agents`
   Y luego intenta nuevamente.

Si tienes problemas, he incluido una Guía llamada [troubleshooting.ipynb](troubleshooting.ipynb) para resolverlos.

Por favor, envíame un mensaje en [https://www.linkedin.com/in/juan-gabriel-gomila-salas/](https://www.linkedin.com/in/juan-gabriel-gomila-salas/) si esto no funciona o si puedo ayudarte en algo. Estoy deseando saber cómo te va.

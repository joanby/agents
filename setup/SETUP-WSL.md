## Domina la Ingeniería de IA Agente - Construye Agentes Autónomos de IA

# Configuración de WSL - Windows Subsystem for Linux

*NOTA 1: Estas instrucciones asumen que ya has seguido las instrucciones de configuración para PC.*

*NOTA 2: En Cursor, recuerda hacer clic derecho en este archivo en el Explorador y seleccionar "Abrir vista previa" para ver el formato.*

¡Bienvenidos de nuevo al mundo de la configuración, usuarios de PC!

Supongo que estás aquí porque has llegado a la Semana 6, y has descubierto la desagradable noticia de que los Servidores MCP solo funcionan en Windows bajo WSL.

¡Lamento mucho hacerte pasar por esto! La buena noticia es que varios estudiantes han confirmado que los Servidores MCP están funcionando bajo WSL. Además, WSL es generalmente considerado una excelente forma de desarrollar en Windows. Y la otra buena noticia es que ya has hecho la configuración una vez, ¡así que seguramente esto será relativamente indoloro! Cruzo los dedos.

### Parte 1: Instalar WSL si aún no lo has hecho

WSL es la forma recomendada por Microsoft para ejecutar Linux en tu PC con Windows, tal como se describe aquí:
[https://learn.microsoft.com/en-us/windows/wsl/install](https://learn.microsoft.com/en-us/windows/wsl/install)

Usaremos la distribución predeterminada de Ubuntu, que parece funcionar bien. ¡Vamos allá!

1. Abre PowerShell
2. Ejecuta: `wsl --install`
3. Selecciona permitir permisos elevados cuando se te pida; luego espera a que Ubuntu se instale.
4. Luego ejecuta `wsl` para iniciarlo y establecer tu nombre de usuario y contraseña de Linux.
5. Escribe `pwd` y `ls` para ver en qué directorio estás y listar los contenidos. Luego escribe `cd` para cambiar a tu directorio personal y repite.

Es importante entender la diferencia entre tu directorio personal de Windows y este nuevo directorio en tu mundo Linux bajo WSL.

### Parte 2: Instalar uv y el repositorio

1. Desde PowerShell, ejecuta `ubuntu` – ten en cuenta que es importante usar `ubuntu` y no `wsl`, ya que te inicia en tu directorio personal de Linux.
2. Luego sigue las instrucciones para Linux aquí: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/) y ejecuta `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Después de que se complete la instalación, necesitas escribir `exit` para salir de WSL y regresar a PowerShell, luego escribe `ubuntu` para regresar a Linux y que se reconozcan los cambios en el PATH.
4. Ahora escribe `pwd` para verificar que estás en tu directorio personal de Linux. Si tienes dudas, usa `cd ~` y `ls` para verificar.
5. Ahora crea un directorio de proyectos con `mkdir projects` y luego `cd projects` para ingresar a él.
6. Y desde tu nuevo directorio de proyectos, clona el repositorio con `git clone https://github.com/ed-donner/agents.git`
7. Ahora ingresa en tu nuevo directorio `agents`, tu Directorio Raíz del Proyecto, con `cd agents`.
8. Y ahora ejecuta el todopoderoso `uv sync`.

En este punto, experimenté un error desagradable de memoria. Creo que está relacionado con mi configuración y no deberías tenerlo. Pero si lo experimentas, por favor avísame, ¡tengo una solución!

### Parte 3: Configurar Cursor ejecutándose en tu entorno de PC

1. Abre Cursor de la manera habitual en tu PC.
2. Abre el panel de extensiones (Menú de vista >> Extensiones o Ctrl+Shift+X), busca WSL, busca WSL de Anysphere (los creadores de Cursor) e instálalo.
3. Ahora presiona Ctrl+Shift+P y busca Remote-WSL: New Window y selecciona esta opción para abrir una nueva ventana configurada para WSL.
4. Selecciona "Abrir Proyecto" (y ve a por un café), navega a tu nuevo directorio raíz del proyecto "agents" en Linux y luego haz clic en "Abrir" o "Seleccionar Carpeta".
5. Vuelve a abrir el panel de extensiones (Ctrl+Shift+X) e instala estas extensiones en tu WSL si no están ya instaladas: Python (ms-python) y Jupyter (microsoft), haciendo clic en el botón "Instalar en WSL-Ubuntu".

### ¡Y ahora deberías estar listo para comenzar!

Necesitarás crear un nuevo archivo ".env" en la carpeta `agents` y copiar tu archivo .env desde tu otro proyecto. Además, necesitarás hacer clic en "Seleccionar Kernel" y "Elegir entorno de python...".

¡Disfruta de MCP!

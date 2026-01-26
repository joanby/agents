# Direttorio Crew

Crew de agentes [CrewAI](https://crewai.com) para **plan editorial de 15–20 días**, **artículos SEO** escritos por **copywriter profesional**, **manager (visto bueno)** y **actualización automática del calendario**. Diseñado para directorios/magazines que necesitan contenido SEO optimizado con enlaces internos.

## ¿Qué hace la crew?

- **Plan editorial**: un **especialista** crea un calendario de 15–20 días. Cada día puede tener un artículo (tema + breve) o descanso. Un día un artículo, otro día otro artículo.
- **Pipeline de artículo** (para cada día):
  1. Plan estratégico → investigación keywords → investigación contenido
  2. **Copywriter profesional** escribe el artículo (800–1200+ palabras, SEO, CTA)
  3. **Editor SEO** → **Especialista en enlaces** → **Corrector de calidad**
  4. **Manager** (LLM potente, ej. GPT-4o) da el **visto bueno**: APROBADO / NO APROBADO + motivación
  5. **Actualizador de calendario** actualiza el plan editorial (día marcado como hecho, enlace artículo, resultado manager)

Los artículos se guardan como `output/articulo_dia_N.md`. El calendario en `output/calendario_editorial.md` se actualiza después de cada artículo.

## Requisitos

- Python ≥3.10 <3.14
- [UV](https://docs.astral.sh/uv/) (recomendado) o pip

## Instalación

```bash
pip install uv
cd 3_crew/direttorio
uv sync
# o: crewai install
```

Copia `.env.example` a `.env` y configura `OPENAI_API_KEY` (obligatorio). Opcionales: `SEMRUSH_API_KEY`, `SERPER_API_KEY`.

## Configuración inicial

### 1. Personalizar datos del directorio

**`knowledge/contexto_directorio.md`**: Este archivo contiene un **template con datos de ejemplo**. Debes reemplazarlo con tus datos reales:

- **Categorías**: Reemplaza `categoria1`, `categoria2`, etc. con tus categorías reales. Asegúrate de que los slugs coincidan con tu estructura de URLs (ej. `/categorias/{slug}`).
- **Ciudades**: Reemplaza `ciudad1`, `ciudad2`, etc. con tus ciudades reales.
- **Creadores**: Reemplaza `creador1`, `creador2`, etc. con tus creadores/perfiles reales. Incluye slug, nombre, categoría y ciudad.

**Formato de URLs**: Ajusta las URLs base (`/categorias/`, `/ciudades/`, `/perfiles/`) según tu aplicación. El sistema usa estos patrones para generar enlaces internos en los artículos.

**Cómo poblar**:
- **Manual**: Edita el archivo directamente.
- **Script**: Crea un script que exporte desde tu base de datos y genere este archivo.
- **API**: Si tu directorio tiene API, crea un script que la consulte.

### 2. Keywords (opcional)

**`knowledge/keywords.csv`**: Fallback para investigación de keywords si no usas SEMrush. El archivo incluye ejemplos placeholder. Reemplázalos con tus keywords reales.

**Formato**:
```csv
keyword,volume,cpc,competition
tu keyword principal,3200,0.5,medium
otra keyword,1100,0.3,low
```

**Columnas**:
- `keyword`: La palabra clave
- `volume`: Volumen de búsqueda (opcional, puede ser "-")
- `cpc`: Costo por clic (opcional, puede ser "-")
- `competition`: Nivel de competencia (opcional: low, medium, high, o "-")

### 3. Preferencias de usuario

**`knowledge/preferencias_usuario.txt`**: Tono, idioma y objetivos. Personaliza según tu marca:
- Idioma: español (o el idioma de tu audiencia)
- Tono: profesional, elegante, accesible, etc.
- Estilo: párrafos breves, listas, evitar anglicismos, etc.

## Ejecución

Desde la raíz del proyecto (`3_crew/direttorio`). Usa **`uv run`** para usar el venv del proyecto:

**Solo plan editorial (15–20 días):**
```bash
uv run run_cli --calendar-only
# o: uv run run_cli -c --num-days 20
```

**Artículo para el día N** (tema del calendario):
```bash
uv run run_cli --day 3
# o: uv run run_cli -n 5
```

**Override tema** (también sin calendario):
```bash
uv run run_cli --day 1 --topic "Tu tema personalizado"
```

**Con crewai run** (env):
```bash
CALENDAR_ONLY=1 crewai run
DAY=3 crewai run
```

## Output

- **`output/calendario_editorial.md`**: Plan editorial; actualizado después de cada artículo.
- **`output/articulo_dia_N.md`**: Artículo para el día N.
- **`output/decision_manager.md`**: APROBADO / NO APROBADO + motivación.
- **`output/plan_estrategico.md`**: Plan estratégico del último artículo.

## Manager (visto bueno)

El **manager** usa un LLM potente (**GPT-4o** en `agents.yaml`). Evalúa calidad, SEO, tono y completitud y retorna APROBADO o NO APROBADO con breve motivación. No hay loop automático: en caso de NO APROBADO puedes modificar inputs/tareas y relanzar.  
*(Si en el futuro quieres usar un modelo más fuerte tipo GPT-5, solo actualiza `llm` para el agente `manager`.)*

## SEMrush vs CSV

- **Con `SEMRUSH_API_KEY`**: La herramienta usa la API SEMrush (reporte `phrase_all`) para el tema del artículo.
- **Sin API**: Lee `knowledge/keywords.csv` (o `KEYWORDS_CSV`). Filtra por tema si es posible, de lo contrario retorna todas las keywords. Formato mínimo: `keyword,volume,cpc,competition`.

## Variables de entorno

- `OPENAI_API_KEY` (obligatorio)
- `SEMRUSH_API_KEY` (opcional)
- `SERPER_API_KEY` (opcional)
- `DIRECTORY_CONTEXT_PATH` (default: `knowledge/contexto_directorio.md`)
- `USER_PREFERENCE_PATH` (default: `knowledge/preferencias_usuario.txt`)
- `KEYWORDS_CSV` (default: `knowledge/keywords.csv`)
- `CALENDAR_PATH` (default: `output/calendario_editorial.md`)
- `NUM_DAYS` (default: 20)
- `TOPIC` (override tema)
- `DAY` (día para ejecutar)
- `CALENDAR_ONLY` (1 para solo calendario)

## Test

```bash
uv run python -m unittest direttorio.tools.test_keyword_research_tool -v
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'direttorio'`**: Estás usando un venv donde el paquete no está instalado (ej. el del workspace padre). Ejecuta siempre desde `3_crew/direttorio` con **`uv run run_cli ...`** o **`uv run python -m direttorio.main ...`** para usar el venv del proyecto.

## Reporte y commit (GitHub)

1. Crea un branch dedicado (ej. `content/directory-articles`).
2. Ejecuta `--calendar-only`, luego `--day 1`, `--day 3`, … para los artículos.
3. Incluye `output/calendario_editorial.md`, `output/articulo_dia_*.md`, `output/decision_manager.md` en commit/PR o impórtalos al magazine.

## Estructura del proyecto

- `src/direttorio/config/`: `agents.yaml`, `tasks.yaml`, `tasks_calendar.yaml` (solo Calendar crew)
- `src/direttorio/crew.py`: **DirettorioCalendarCrew** (solo calendario), **DirettorioArticleCrew** (pipeline artículo + manager + actualización calendario)
- `src/direttorio/main.py`: `--calendar-only`, `--day N`, `--topic`
- `src/direttorio/tools/keyword_research_tool.py`: SEMrush + CSV fallback
- `knowledge/`: `contexto_directorio.md` (template), `keywords.csv` (ejemplos), `preferencias_usuario.txt`

## Personalización

### Paso 1: Configurar contexto del directorio

Edita `knowledge/contexto_directorio.md` y reemplaza:
- Categorías: `categoria1`, `categoria2` → tus categorías reales
- Ciudades: `ciudad1`, `ciudad2` → tus ciudades reales
- Creadores: `creador1`, `creador2` → tus creadores/perfiles reales
- URLs base: Ajusta `/categorias/`, `/ciudades/`, `/perfiles/` según tu aplicación

### Paso 2: Configurar keywords (opcional)

Si no usas SEMrush, edita `knowledge/keywords.csv` con tus keywords reales. Formato: `keyword,volume,cpc,competition`.

### Paso 3: Personalizar preferencias

Edita `knowledge/preferencias_usuario.txt` con tu tono, idioma y estilo preferidos.

### Paso 4: Ejecutar

```bash
uv run run_cli --calendar-only
uv run run_cli --day 1
```

## Flujo de trabajo recomendado

1. **Primera vez**: Personaliza `contexto_directorio.md`, `keywords.csv` (opcional), `preferencias_usuario.txt`.
2. **Generar plan**: `uv run run_cli --calendar-only` → `output/calendario_editorial.md`.
3. **Revisar plan**: Ajusta manualmente si es necesario.
4. **Generar artículos**: `uv run run_cli --day 1`, `--day 3`, etc. Cada ejecución actualiza el calendario.
5. **Revisar artículos**: `output/articulo_dia_*.md` y `output/decision_manager.md`.
6. **Publicar**: Importa los artículos aprobados a tu CMS/magazine.

## Soporte

- [Documentación CrewAI](https://docs.crewai.com)
- [CrewAI en GitHub](https://github.com/joaomdmoura/crewai)
- [Discord CrewAI](https://discord.com/invite/X4JWnZnxPb)

# =============================================================================
# CV Interactivo — Agente Principal con Evaluación Multi-Agente
# Arquitectura híbrida Groq (primario) + Ollama Cloud (fallback)
# =============================================================================
#
#  PIPELINE POR TURNO
#  ──────────────────
#
#   mensaje entrada
#        │
#   [PASO 1] ─── Toxicidad ──────────────────────────────────────────────────┐
#        │       Groq: llama-prompt-guard-2-22m  (22M params, <100ms)        │
#        │       Fallback: Ollama gpt-oss:20b-cloud                          │
#        │       score > 0.7 → bloqueo inmediato                             │
#        │                                                                   │
#   [PASO 2] ─── Agente principal + tool loop ──────────────────────────────┤
#        │       Groq: gpt-oss-120b  (~0.60s TTFT, tool_calls)              │
#        │       Fallback: Ollama nemotron-3-super:120b-cloud (MoE 12B act.) │
#        │                                                                   │
#   [PASO 3] ─── Evaluación de calidad  ────────────────────────────────────┤
#        │       Groq: gpt-oss-20b  (945 t/s output, JSON corto)            │
#        │       Fallback: Ollama gpt-oss:20b-cloud                          │
#        │       quality_score < 0.6 → rerun                                │
#        │                                                                   │
#   [PASO 4] ─── Rerun opcional ─────────────────────────────────────────────┘
#               Ollama: nemotron-3-super:120b-cloud
#               (rerun es infrecuente; Groq no merece cuota aquí)
#
#  GESTIÓN DE RATE LIMITS (tier gratuito Groq)
#  ────────────────────────────────────────────
#   Contadores RPM/RPD por modelo con ventana deslizante.
#   Al alcanzar el 80% del límite → fallback automático a Ollama.
#   Sin 429s, sin latencia extra por reintentos.
#
# =============================================================================

import json
import os
import time
import logging
import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

import requests
from dotenv import load_dotenv
from openai import OpenAI
from jinja2 import Template
import gradio as gr

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================

load_dotenv(override=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("angel_cv")

# ── Clientes LLM ──────────────────────────────────────────────────────────────

_groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"),
)

_ollama_client = OpenAI(
    base_url=os.environ.get("OLLAMA_BASE_URL", "https://ollama.com/v1"),
    api_key=os.environ.get("OLLAMA_API_KEY"),
)

# ── Modelos por rol ───────────────────────────────────────────────────────────
#
#  Selección razonada:
#
#  toxicity:
#    - Groq llama-prompt-guard-2-22m: 22M params especializado en toxicidad.
#      Latencia <100ms, 15K TPM propios — no consume cuota de los otros modelos.
#    - Fallback: Ollama gpt-oss:20b-cloud.
#
#  evaluator (calidad):
#    - Groq gpt-oss-20b: 945 t/s output, TTFT ~0.30s. El evaluador genera
#      JSON corto (<150 tokens), throughput altísimo = respuesta casi inmediata.
#    - Fallback: Ollama gpt-oss:20b-cloud.
#
#  agent (principal):
#    - Groq gpt-oss-120b: TTFT ~0.60s, soporta tool_calls. Mínima latencia
#      percibida para el usuario.
#    - Fallback: Ollama nemotron-3-super:120b-cloud — MoE 120B total,
#      solo 12B params activos por token. Mejor ratio calidad/velocidad de Ollama.
#
#  rerun:
#    - Solo Ollama: el rerun es infrecuente. Conservar cuota Groq para el
#      flujo principal tiene mayor impacto en la experiencia real.

MODELS: dict[str, dict[str, tuple[str, str]]] = {
    "toxicity": {
        # llama-prompt-guard-2-22m es clasificador binario (SAFE/UNSAFE),
        # no genera JSON — incompatible con user_toxicity.md.
        # Se unifica con gpt-oss-20b que sí sigue instrucciones de formato.
        "primary":  ("groq",   "openai/gpt-oss-20b"),
        "fallback": ("ollama", "gpt-oss:20b-cloud"),
    },
    "evaluator": {
        "primary":  ("groq",   "openai/gpt-oss-20b"),
        "fallback": ("ollama", "gpt-oss:20b-cloud"),
    },
    "agent": {
        "primary":  ("groq",   "openai/gpt-oss-120b"),
        "fallback": ("ollama", "nemotron-3-super:120b-cloud"),
    },
    "rerun": {
        "primary":  ("ollama", "nemotron-3-super:120b-cloud"),
        "fallback": ("ollama", "gpt-oss:120b-cloud"),
    },
}

# ── Umbrales ──────────────────────────────────────────────────────────────────

TOXICITY_THRESHOLD = 0.7   # toxicity_score > umbral → bloqueo
QUALITY_THRESHOLD  = 0.6   # quality_score  < umbral → rerun

# ── Pushover ──────────────────────────────────────────────────────────────────

_pushover_user  = os.getenv("PUSHOVER_USER")
_pushover_token = os.getenv("PUSHOVER_TOKEN")
_pushover_url   = "https://api.pushover.net/1/messages.json"

TOXICITY_BLOCK_MESSAGE = (
    "Lo siento, no puedo continuar con esta conversación en estos términos. "
    "Si tienes alguna pregunta profesional, estaré encantado de ayudarte."
)

# =============================================================================
# RATE LIMIT TRACKER — ventana deslizante, thread-safe
# =============================================================================
#
#  Límites gratuitos Groq (tabla de referencia):
#    llama-prompt-guard-2-22m → 30 RPM / 14.4K RPD / 15K TPM
#    gpt-oss-20b              → 30 RPM /  8K RPD  / 200K TPD
#    gpt-oss-120b             → 30 RPM /  8K RPD  / 200K TPD
#
#  Factor de seguridad 80%: forzamos fallback antes de recibir un 429,
#  eliminando la latencia extra de error + retry.

_GROQ_LIMITS: dict[str, dict[str, int]] = {
    "meta-llama/llama-prompt-guard-2-22m": {"rpm": 30,  "rpd": 14_400},
    "openai/gpt-oss-20b":                  {"rpm": 30,  "rpd":  8_000},
    "openai/gpt-oss-120b":                 {"rpm": 30,  "rpd":  8_000},
}
_SAFETY_FACTOR = 0.80


class _RateLimitTracker:
    """
    Contabiliza llamadas Groq por modelo con ventana deslizante (monotonic).
    Thread-safe mediante Lock.
    """

    def __init__(self) -> None:
        self._lock   = threading.Lock()
        self._rpm_ts: dict[str, deque] = {}
        self._rpd_ts: dict[str, deque] = {}

    def _ensure(self, model: str) -> None:
        if model not in self._rpm_ts:
            self._rpm_ts[model] = deque()
            self._rpd_ts[model] = deque()

    @staticmethod
    def _purge(dq: deque, window: float) -> None:
        cutoff = time.monotonic() - window
        while dq and dq[0] < cutoff:
            dq.popleft()

    def can_use(self, model: str) -> bool:
        """True si el modelo tiene margen dentro del 80% del límite."""
        limits = _GROQ_LIMITS.get(model)
        if not limits:
            return True
        with self._lock:
            self._ensure(model)
            self._purge(self._rpm_ts[model], 60.0)
            self._purge(self._rpd_ts[model], 86_400.0)
            rpm_ok = len(self._rpm_ts[model]) < limits["rpm"] * _SAFETY_FACTOR
            rpd_ok = len(self._rpd_ts[model]) < limits["rpd"] * _SAFETY_FACTOR
            return rpm_ok and rpd_ok

    def record(self, model: str) -> None:
        """Registra una llamada completada."""
        if model not in _GROQ_LIMITS:
            return
        with self._lock:
            self._ensure(model)
            ts = time.monotonic()
            self._rpm_ts[model].append(ts)
            self._rpd_ts[model].append(ts)

    def status(self) -> dict:
        """Estado actual de uso para logging/debug."""
        out = {}
        with self._lock:
            for model, limits in _GROQ_LIMITS.items():
                self._purge(self._rpm_ts.get(model, deque()), 60.0)
                self._purge(self._rpd_ts.get(model, deque()), 86_400.0)
                out[model] = {
                    "rpm_used":  len(self._rpm_ts.get(model, [])),
                    "rpm_limit": limits["rpm"],
                    "rpd_used":  len(self._rpd_ts.get(model, [])),
                    "rpd_limit": limits["rpd"],
                }
        return out


_rate_tracker = _RateLimitTracker()

# =============================================================================
# CLIENTE HÍBRIDO — selección automática con fallback
# =============================================================================

def _get_client(provider: str) -> OpenAI:
    return _groq_client if provider == "groq" else _ollama_client


def _llm_call(role: str, **kwargs) -> object:
    """
    Llamada LLM con selección automática de proveedor.

    Lógica:
      1. Si el primario es Groq y tiene margen → llamar con Groq.
      2. Si la llamada falla → loguear y caer en fallback.
      3. Si el rate limit está al 80% → saltar a fallback directamente.
      4. Si ambos fallan → propagar excepción.

    Args:
        role:   clave en MODELS dict
        kwargs: parámetros para client.chat.completions.create()
    """
    config   = MODELS[role]
    p_prov, p_model = config["primary"]
    f_prov, f_model = config["fallback"]

    use_primary = (p_prov != "groq") or _rate_tracker.can_use(p_model)

    if use_primary:
        try:
            resp = _get_client(p_prov).chat.completions.create(model=p_model, **kwargs)
            if p_prov == "groq":
                _rate_tracker.record(p_model)
            logger.debug("✓ [%s] %s/%s", role, p_prov, p_model)
            return resp
        except Exception as exc:
            logger.warning("✗ [%s] %s/%s falló (%s) → fallback", role, p_prov, p_model, exc)
    else:
        logger.info("⚡ Rate limit Groq (%s) → fallback directo", p_model)

    # Fallback
    resp = _get_client(f_prov).chat.completions.create(model=f_model, **kwargs)
    logger.debug("✓ fallback [%s] %s/%s", role, f_prov, f_model)
    return resp

# =============================================================================
# PUSHOVER
# =============================================================================

def _push(message: str) -> None:
    logger.info("Pushover → %s", message)
    try:
        r = requests.post(
            _pushover_url,
            data={"user": _pushover_user, "token": _pushover_token, "message": message},
            timeout=5,
        )
        r.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("Pushover error: %s", exc)

# =============================================================================
# TOOLS DEL AGENTE PRINCIPAL
# =============================================================================

def record_user_details(
    email: str,
    name:  str = "Nombre no proporcionado",
    notes: str = "not provided",
) -> dict:
    _push(f"Contacto registrado → {name} | {email} | {notes}")
    return {"recorded": "ok"}


def record_unknown_question(question: str) -> dict:
    _push(f"Pregunta sin respuesta → {question}")
    return {"recorded": "ok"}


_TOOL_REGISTRY: dict[str, callable] = {
    "record_user_details":     record_user_details,
    "record_unknown_question": record_unknown_question,
}

_TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "record_user_details",
            "description": (
                "Úsala cuando el usuario proporcione su email para ser contactado. "
                "Registra nombre, email y contexto de la conversación."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Email del usuario."},
                    "name":  {"type": "string", "description": "Nombre del usuario, si lo ha dado."},
                    "notes": {"type": "string", "description": "Contexto relevante para el seguimiento."},
                },
                "required": ["email"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "record_unknown_question",
            "description": (
                "Úsala cuando no puedas responder una pregunta del usuario. "
                "Registra la pregunta para revisión posterior."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "Pregunta sin respuesta."},
                },
                "required": ["question"],
                "additionalProperties": False,
            },
        },
    },
]

# =============================================================================
# PROMPTS — caché Jinja2
# =============================================================================

@lru_cache(maxsize=8)
def _load_template(path: str) -> Template:
    return Template(Path(path).read_text(encoding="utf-8"))


def _render_prompt(path: str, **kwargs) -> str:
    return _load_template(path).render(**kwargs)


def get_system_prompt() -> str:
    return _render_prompt("prompts/meBest.md")


# Resumen compacto del perfil para los evaluadores.
# El me.md completo (~200 líneas, ~4000 tokens) + historial + mensaje + reply
# superaba el límite de contexto de gpt-oss-20b en Groq → content=None.
# Este resumen ocupa ~300 tokens y contiene todo lo necesario para evaluar
# si una respuesta es fiel al perfil.
_AGENT_CONTEXT_COMPACT = (
    "Angel Nacar Jimenez — Senior Software Developer & Scrum Master, Madrid. "
    "9+ años experiencia total. "

    # Experiencia verificable
    "Babel (2021-actualidad): Senior Dev + Scrum Master, lider tecnico ~5 personas, "
    "sistemas criticos GISS, Java (Pros@/J2EE), PL/SQL Oracle, JS, XSL, "
    "Git, Dimensions, UML, Eclipse IBM RSA. "
    "FEI (2018-2021): Developer, entorno GISS, Java Pros@, PL/SQL, SVN. "
    "Continex (2016-2018): Full Stack, Java Spring, AngularJS, SQL. "

    # Certificaciones y skills verificables
    "AWS Certified Cloud Practitioner. Scrum certificado. "
    "IA aplicada: agentes, automatizacion con n8n (proyecto 'The Last Byte'). "
    "Ubicacion: Madrid. Busca retos complejos con Cloud e IA. "

    # Reglas anti-alucinacion para el evaluador
    "REGLAS: No tiene experiencia en empresas distintas a las listadas. "
    "No tiene certificaciones distintas a AWS CP. "
    "No domina tecnologias no listadas. Tono profesional y cercano."
)


def _prompt_toxicity(message: str, history: list) -> str:
    return _render_prompt("prompts/user_toxicity.md", message=message, history=history)


def _prompt_quality(history: list, message: str, reply: str) -> str:
    # Firma simplificada: ya no recibe agent_context como parámetro,
    # usa siempre _AGENT_CONTEXT_COMPACT para controlar el tamaño del prompt.
    return _render_prompt(
        "prompts/agent_quality.md",
        agent_context=_AGENT_CONTEXT_COMPACT,
        history=history,
        message=message,
        reply=reply,
    )


def _parse_json_safe(raw: str | None, label: str) -> dict | None:
    """
    Parse JSON defensivo contra los tres casos de fallo observados en Groq:
      1. content=None  → Groq truncó por límite de contexto/output
      2. string vacío  → modelo no generó nada
      3. bloques ```json ... ```  → algunos modelos añaden markdown
    Devuelve None si no se puede parsear; el caller aplica el fallback.
    """
    if not raw:
        logger.warning("%s: content=None o vacío (Groq truncó la respuesta)", label)
        return None
    cleaned = raw.strip()
    if "```" in cleaned:
        # Extraer contenido entre los primeros backticks
        parts = cleaned.split("```")
        if len(parts) >= 2:
            cleaned = parts[1].strip()
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.warning("%s: JSONDecodeError — raw=%r — %s", label, raw[:300], exc)
        return None

# =============================================================================
# DISPATCH DE TOOL CALLS
# =============================================================================

def _handle_tool_calls(tool_calls) -> list[dict]:
    results = []
    for tc in tool_calls:
        name = tc.function.name
        try:
            args = json.loads(tc.function.arguments)
        except json.JSONDecodeError as exc:
            logger.error("Error parseando args de '%s': %s", name, exc)
            args = {}

        logger.info("Tool → %s | %s", name, args)
        fn = _TOOL_REGISTRY.get(name)

        if fn is None:
            logger.warning("Tool desconocida ignorada: %s", name)
            result = {"error": f"tool '{name}' no registrada"}
        else:
            try:
                result = fn(**args)
            except Exception as exc:
                logger.error("Error ejecutando '%s': %s", name, exc)
                result = {"error": str(exc)}

        results.append({
            "role": "tool", "content": json.dumps(result), "tool_call_id": tc.id,
        })
    return results

# =============================================================================
# AGENTES EVALUADORES
# =============================================================================

def _evaluate_toxicity(message: str, history: list) -> dict:
    """
    Evaluador de toxicidad. Output JSON: { classification, toxicity_score, reason }
    Usa _parse_json_safe para manejar content=None de Groq.
    """
    try:
        resp = _llm_call(
            "toxicity",
            messages=[
                {
                    "role":    "system",
                    "content": "Eres un evaluador de seguridad. Responde SOLO con JSON valido, sin texto adicional.",
                },
                {
                    "role":    "user",
                    "content": _prompt_toxicity(message, history),
                },
            ],
            max_tokens=150,
            temperature=0.0,
        )
        raw    = resp.choices[0].message.content
        parsed = _parse_json_safe(raw, "toxicity")
        if parsed is not None:
            return parsed
    except Exception as exc:
        logger.error("Evaluador toxicidad falló: %s", exc)
    # Fail-open: si falla no bloqueamos al usuario
    return {"classification": "ACCEPTABLE", "toxicity_score": 0.0, "reason": "evaluador no disponible"}


def _evaluate_quality(reply: str, message: str, history: list) -> dict:
    """
    Evaluador de calidad de la respuesta del agente.
    Modelo: gpt-oss-20b (Groq) — 945 t/s, ideal para JSON corto.
    Usa _parse_json_safe y contexto compacto para evitar content=None.
    Output JSON: { classification, quality_score, issues, suggestion }
    """
    try:
        resp = _llm_call(
            "evaluator",
            messages=[
                {
                    "role":    "system",
                    "content": _prompt_quality(history, message, reply),
                },
                {
                    "role":    "user",
                    "content": "Evalua la respuesta segun las instrucciones y devuelve el JSON.",
                },
            ],
            max_tokens=300,
            temperature=0.0,
        )
        raw    = resp.choices[0].message.content
        parsed = _parse_json_safe(raw, "quality")
        if parsed is not None:
            return parsed
    except Exception as exc:
        logger.error("Evaluador calidad falló: %s", exc)
    # Fail-safe: si falla aceptamos la respuesta
    return {"classification": "GOOD", "quality_score": 1.0, "issues": [], "suggestion": ""}

# =============================================================================
# RERUN — regeneración con feedback del evaluador
# =============================================================================

def _rerun(reply: str, message: str, history: list, feedback: str) -> str:
    """
    Regenera la respuesta incorporando el feedback del evaluador.
    Usa Ollama exclusivamente — el rerun es infrecuente, conservamos cuota Groq.
    """
    augmented = (
        f"{get_system_prompt()}\n\n"
        "## ⚠️ Respuesta anterior rechazada por control de calidad\n\n"
        f"**Respuesta rechazada:**\n{reply}\n\n"
        f"**Motivo del rechazo:**\n{feedback}\n\n"
        "Genera una nueva respuesta corrigiendo los problemas indicados. "
        "Mantén el mismo tono profesional y cercano."
    )
    try:
        resp = _llm_call(
            "rerun",
            messages=(
                [{"role": "system", "content": augmented}]
                + history
                + [{"role": "user", "content": message}]
            ),
        )
        return resp.choices[0].message.content
    except Exception as exc:
        logger.error("Rerun falló: %s — manteniendo respuesta original", exc)
        return reply

# =============================================================================
# AGENTE PRINCIPAL — chat()
# =============================================================================

def chat(message: str, history: list) -> str:
    """
    Función principal del chatbot CV Ángel Nácar.

    Pipeline:
      1. Toxicidad      → Groq prompt-guard-22m  (< 100ms, cuota propia)
      2. Agente         → Groq gpt-oss-120b      (TTFT ~0.60s, tool_calls)
         └ tool loop    → ejecuta tools locales si el agente las invoca
      3. Calidad        → Groq gpt-oss-20b       (945 t/s, JSON corto)
      4. Rerun opcional → Ollama nemotron-3-super (si quality_score < 0.6)
      5. Rate limits    → fallback automático a Ollama si Groq alcanza 80%

    Args:
        message: turno actual del usuario
        history: historial [{role, content}, ...]
    Returns:
        Respuesta final como string.
    """

    # ── PASO 1: Toxicidad ─────────────────────────────────────────────────────
    user_eval      = _evaluate_toxicity(message, history)
    toxicity_score = user_eval.get("toxicity_score", 0.0)

    logger.info(
        "Toxicidad → %s | score=%.2f | %s",
        user_eval.get("classification"), toxicity_score, user_eval.get("reason", ""),
    )

    if toxicity_score > TOXICITY_THRESHOLD:
        logger.warning("Mensaje BLOQUEADO (toxicity=%.2f)", toxicity_score)
        return TOXICITY_BLOCK_MESSAGE

    # ── PASO 2: Agente principal con tool loop ────────────────────────────────
    #
    # BUG FIX — historial de Gradio contiene metadatos propietarios.
    # Gradio type="messages" inyecta campos extra en cada mensaje del historial
    # (metadata, id, etc.) que Groq rechaza con HTTP 400 en messages.N.
    # Se sanitiza el historial extrayendo solo role+content antes de enviarlo.
    def _sanitize_history(hist: list) -> list:
        clean = []
        for m in hist:
            if isinstance(m, dict) and "role" in m and "content" in m:
                clean.append({"role": m["role"], "content": m["content"] or ""})
        return clean

    messages = (
        [{"role": "system", "content": get_system_prompt()}]
        + _sanitize_history(history)
        + [{"role": "user", "content": message}]
    )

    reply = None

    for iteration in range(10):
        try:
            response = _llm_call("agent", messages=messages, tools=_TOOLS_SCHEMA)
        except Exception as exc:
            logger.error("Agente falló en iteración %d: %s", iteration, exc)
            return "Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo."

        choice        = response.choices[0]
        finish_reason = choice.finish_reason

        if finish_reason == "tool_calls":
            assistant_msg = choice.message
            tool_results  = _handle_tool_calls(assistant_msg.tool_calls)
            # Serializar a dict limpio — misma razón que el historial de Gradio:
            # los objetos del SDK de OpenAI incluyen campos (metadata, logprobs…)
            # que Groq rechaza. Solo se pasan role, content y tool_calls.
            messages.append({
                "role":       "assistant",
                "content":    assistant_msg.content or "",
                "tool_calls": [
                    {
                        "id":       tc.id,
                        "type":     "function",
                        "function": {
                            "name":      tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in assistant_msg.tool_calls
                ],
            })
            messages.extend(tool_results)
            continue

        reply = choice.message.content
        break

    if not reply:
        logger.error("Sin respuesta textual tras 10 iteraciones")
        return "Lo siento, no he podido generar una respuesta. Por favor, inténtalo de nuevo."

    # ── PASO 3: Calidad ───────────────────────────────────────────────────────
    #
    # BUG FIX — reply puede ser None si el agente solo ejecutó tool_calls
    # sin generar texto final (edge case: tool_call como último turno).
    # El guard `if not reply` de arriba lo cubre, pero se deja el log explícito.
    llm_eval      = _evaluate_quality(reply, message, history)
    quality_score = llm_eval.get("quality_score", 1.0)

    logger.info(
        "Calidad → %s | score=%.2f | issues=%s",
        llm_eval.get("classification"), quality_score, llm_eval.get("issues"),
    )

    # ── PASO 4: Rerun si la calidad no supera el umbral ───────────────────────
    if quality_score < QUALITY_THRESHOLD:
        feedback = llm_eval.get("suggestion") or llm_eval.get("issues", "")
        if isinstance(feedback, list):
            feedback = "; ".join(feedback)
        logger.warning("Respuesta RECHAZADA (score=%.2f) → rerun. Feedback: %s", quality_score, feedback)
        reply = _rerun(reply, message, history, feedback)

    # ── PASO 5: Estado de rate limits (debug) ─────────────────────────────────
    logger.debug("Rate limits Groq: %s", _rate_tracker.status())

    return reply

# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    from ui import build_ui
    app = build_ui(chat)
    app.launch(server_name="0.0.0.0", server_port=7860)

#!/usr/bin/env python
"""Ejecutar crew Direttorio: solo calendario o artículo para día N (con manager + actualización calendario)."""

from __future__ import annotations

import argparse
import os
import re
import sys
import warnings
from datetime import datetime
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_KNOWLEDGE = _PROJECT_ROOT / "knowledge"
_OUTPUT = _PROJECT_ROOT / "output"

try:
    from dotenv import load_dotenv
    load_dotenv(_PROJECT_ROOT / ".env")
except ImportError:
    pass

from direttorio.crew import DirettorioArticleCrew, DirettorioCalendarCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def _load_text(path: Path, default: str = "") -> str:
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    return default


def _parse_topic_for_day(calendar_md: str, day: int) -> str | None:
    """Extrae el tema para el día N del plan editorial (markdown). Retorna None si es descanso."""
    pattern = rf"(?ms)##\s*Día\s+{day}\b.*?(?=##\s*Día\s+\d+|$)"
    m = re.search(pattern, calendar_md)
    if not m:
        return None
    block = m.group(0)
    if re.search(r"descanso|sin\s+artículo|ningún\s+artículo", block, re.I):
        return None
    topic_m = re.search(r"\*\*Tema\*\*:\s*(.+?)(?:\n|$)", block)
    if topic_m:
        return topic_m.group(1).strip()
    return None


def run_calendar(
    num_days: int = 20,
    directory_context_path: str | None = None,
) -> None:
    """Genera solo el plan editorial (15-20 días)."""
    base = _PROJECT_ROOT
    ctx_path = Path(
        directory_context_path or os.environ.get("DIRECTORY_CONTEXT_PATH", str(_KNOWLEDGE / "contexto_directorio.md"))
    )
    if not ctx_path.is_absolute():
        ctx_path = base / ctx_path
    directory_context = _load_text(ctx_path, default="(Sin contexto de directorio.)")

    _OUTPUT.mkdir(parents=True, exist_ok=True)
    inputs = {
        "num_days": str(num_days),
        "directory_context": directory_context,
        "current_year": str(datetime.now().year),
    }
    try:
        result = DirettorioCalendarCrew().crew().kickoff(inputs=inputs)
        print("\n\n=== Plan editorial ===\n\n")
        print(result.raw if hasattr(result, "raw") else result)
        print("\n\nGuardado: output/calendario_editorial.md")
    except Exception as e:
        raise RuntimeError(f"Error en crew de calendario: {e}") from e


def run_article_for_day(
    day: int,
    topic_override: str | None = None,
    directory_context_path: str | None = None,
    user_preference_path: str | None = None,
    calendar_path: str | None = None,
) -> None:
    """Ejecuta la pipeline de artículo para el día N (tema del calendario o override) y actualiza el calendario."""
    base = _PROJECT_ROOT
    ctx_path = Path(
        directory_context_path or os.environ.get("DIRECTORY_CONTEXT_PATH", str(_KNOWLEDGE / "contexto_directorio.md"))
    )
    pref_path = Path(
        user_preference_path or os.environ.get("USER_PREFERENCE_PATH", str(_KNOWLEDGE / "preferencias_usuario.txt"))
    )
    cal_path = Path(calendar_path or os.environ.get("CALENDAR_PATH", str(_OUTPUT / "calendario_editorial.md")))
    if not ctx_path.is_absolute():
        ctx_path = base / ctx_path
    if not pref_path.is_absolute():
        pref_path = base / pref_path
    if not cal_path.is_absolute():
        cal_path = base / cal_path

    directory_context = _load_text(ctx_path, default="(Sin contexto de directorio.)")
    user_preference = _load_text(pref_path, default="Idioma: español. Tono: profesional.")
    editorial_calendar = _load_text(cal_path, default="")

    if topic_override:
        topic = topic_override
        if not editorial_calendar:
            editorial_calendar = (
                f"# Plan editorial\n\n## Día {day}\n- **Tema**: {topic_override}\n- **Estado**: por hacer\n"
            )
    elif editorial_calendar:
        topic = _parse_topic_for_day(editorial_calendar, day)
        if not topic:
            raise RuntimeError(
                f"Día {day}: no se encontró tema (¿descanso?) o calendario no válido. "
                "Usa --topic para override."
            )
    else:
        raise RuntimeError(
            "No hay calendario en output/calendario_editorial.md. Ejecuta primero con --calendar-only "
            "o usa --topic."
        )

    _OUTPUT.mkdir(parents=True, exist_ok=True)
    inputs = {
        "directory_context": directory_context,
        "topic": topic,
        "day": str(day),
        "current_year": str(datetime.now().year),
        "user_preference": user_preference,
        "editorial_calendar": editorial_calendar,
    }
    try:
        result = DirettorioArticleCrew().crew().kickoff(inputs=inputs)
        print("\n\n=== Salida ===\n\n")
        print(result.raw if hasattr(result, "raw") else result)
        print(f"\n\nArtículo: output/articulo_dia_{day}.md")
        print("Manager: output/decision_manager.md")
        print("Calendario actualizado: output/calendario_editorial.md")
    except Exception as e:
        raise RuntimeError(f"Error en crew de artículo: {e}") from e


def run(
    topic: str | None = None,
    directory_context_path: str | None = None,
    user_preference_path: str | None = None,
) -> None:
    """
    Ejecuta artículo para tema (sin calendario) o calendario.
    Lee también CALENDAR_ONLY=1 y DAY=N de env (para crewai run).
    """
    if os.environ.get("CALENDAR_ONLY", "").strip().lower() in ("1", "true", "yes"):
        run_calendar(
            num_days=int(os.environ.get("NUM_DAYS", "20")),
            directory_context_path=directory_context_path,
        )
        return
    day_env = os.environ.get("DAY", "").strip()
    if day_env.isdigit():
        run_article_for_day(
            day=int(day_env),
            topic_override=os.environ.get("TOPIC") or topic,
            directory_context_path=directory_context_path,
            user_preference_path=user_preference_path,
            calendar_path=os.environ.get("CALENDAR_PATH") or None,
        )
        return
    if topic:
        run_article_for_day(
            day=1,
            topic_override=topic,
            directory_context_path=directory_context_path,
            user_preference_path=user_preference_path,
            calendar_path="",
        )
        return
    run_calendar(directory_context_path=directory_context_path)


def _main() -> None:
    parser = argparse.ArgumentParser(
        description="Crew Direttorio: plan editorial 15-20 días, artículos por día, manager visto bueno, actualización calendario"
    )
    parser.add_argument("--calendar-only", "-c", action="store_true", help="Solo plan editorial (15-20 días)")
    parser.add_argument("--day", "-n", type=int, default=None, metavar="N", help="Ejecuta pipeline artículo para el día N")
    parser.add_argument("--topic", "-t", default=None, help="Override tema (con --day)")
    parser.add_argument("--num-days", type=int, default=20, metavar="N", help="Días del plan (default 20)")
    parser.add_argument("--directory-context", "-d", dest="directory_context", help="Path contexto_directorio")
    parser.add_argument("--user-preference", "-u", dest="user_preference", help="Path preferencias_usuario")
    parser.add_argument("--calendar-path", dest="calendar_path", help="Path plan editorial (para --day)")
    args = parser.parse_args()

    if args.calendar_only:
        run_calendar(
            num_days=args.num_days,
            directory_context_path=args.directory_context,
        )
    elif args.day is not None:
        run_article_for_day(
            day=args.day,
            topic_override=args.topic,
            directory_context_path=args.directory_context,
            user_preference_path=args.user_preference,
            calendar_path=args.calendar_path,
        )
    else:
        parser.print_help()
        print("\nEjemplos: --calendar-only | --day 3 | --day 5 --topic 'Ejemplo de tema'")


def train() -> None:
    """Entrenar la crew."""
    inputs = {
        "directory_context": _load_text(_KNOWLEDGE / "contexto_directorio.md", "(Sin contexto.)"),
        "topic": os.environ.get("TOPIC", "Ejemplo de tema para artículo"),
        "day": "1",
        "current_year": str(datetime.now().year),
        "user_preference": _load_text(_KNOWLEDGE / "preferencias_usuario.txt", "Idioma: español."),
        "editorial_calendar": _load_text(_OUTPUT / "calendario_editorial.md", ""),
    }
    try:
        DirettorioArticleCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs,
        )
    except Exception as e:
        raise RuntimeError(f"Error en entrenamiento: {e}") from e


def replay() -> None:
    try:
        DirettorioArticleCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise RuntimeError(f"Error en replay: {e}") from e


def test() -> None:
    inputs = {
        "directory_context": _load_text(_KNOWLEDGE / "contexto_directorio.md", "(Sin contexto.)"),
        "topic": os.environ.get("TOPIC", "Ejemplo de tema para artículo"),
        "day": "1",
        "current_year": str(datetime.now().year),
        "user_preference": _load_text(_KNOWLEDGE / "preferencias_usuario.txt", "Idioma: español."),
        "editorial_calendar": _load_text(_OUTPUT / "calendario_editorial.md", ""),
    }
    try:
        DirettorioArticleCrew().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs,
        )
    except Exception as e:
        raise RuntimeError(f"Error en test: {e}") from e


def run_with_trigger() -> None:
    import json
    if len(sys.argv) < 2:
        raise RuntimeError("No hay payload de trigger. Proporciona JSON como argumento.")
    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON inválido: {e}") from e
    inputs = {
        "crewai_trigger_payload": payload,
        "directory_context": _load_text(_KNOWLEDGE / "contexto_directorio.md", ""),
        "topic": "",
        "day": "1",
        "current_year": str(datetime.now().year),
        "user_preference": _load_text(_KNOWLEDGE / "preferencias_usuario.txt", ""),
        "editorial_calendar": "",
    }
    try:
        DirettorioArticleCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise RuntimeError(f"Error en crew: {e}") from e


if __name__ == "__main__":
    _main()

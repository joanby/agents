"""Herramienta de investigación de keywords con fallback CSV para CrewAI Directory crew."""

from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class KeywordResearchToolInput(BaseModel):
    """Esquema de entrada para KeywordResearchTool."""

    query: str = Field(
        ...,
        description="Frase de búsqueda o tema para investigación de keywords (ej. 'ejemplo keyword', 'tema principal').",
    )
    database: str = Field(
        default="us",
        description="Base de datos SEMrush / código de país (ej. 'us' para USA, 'es' para España, 'mx' para México). Solo se usa cuando la API de SEMrush está disponible.",
    )


class KeywordResearchTool(BaseTool):
    """Investigación de keywords vía API SEMrush o fallback CSV.

    Si SEMRUSH_API_KEY está configurado, llama a la API SEMrush phrase_all para la query dada.
    De lo contrario, lee de un archivo CSV (por defecto: knowledge/keywords.csv) con columnas
    keyword, volume, cpc, competition.
    """

    name: str = "Herramienta de Investigación de Keywords"
    description: str = (
        "Investiga keywords SEO para un tema. Usa la API de SEMrush cuando SEMRUSH_API_KEY está configurado, "
        "de lo contrario lee de knowledge/keywords.csv. Retorna una lista en markdown de keywords con "
        "volumen, CPC y competencia para el copywriter y editor SEO."
    )
    args_schema: Type[BaseModel] = KeywordResearchToolInput

    def _run(self, query: str, database: str = "us") -> str:
        api_key = os.getenv("SEMRUSH_API_KEY", "").strip()
        if api_key:
            return self._fetch_semrush(query, database, api_key)
        return self._read_csv(query)

    def _fetch_semrush(self, phrase: str, database: str, api_key: str) -> str:
        """Obtiene datos de keywords de la API SEMrush phrase_all."""
        url = "https://api.semrush.com/"
        params = {
            "type": "phrase_all",
            "key": api_key,
            "phrase": phrase,
            "database": database,
            "export_columns": "Ph,Nq,Cp,Co",
        }
        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            lines = [l.strip() for l in resp.text.strip().split("\n") if l.strip()]
        except Exception as e:
            return (
                f"Error API SEMrush: {e}. Usando fallback CSV. "
                + self._read_csv(phrase)
            )

        if not lines:
            return f"No hay resultados SEMrush para '{phrase}'. " + self._read_csv(phrase)

        # Header: Ph (keyword), Nq (volume), Cp (CPC), Co (competition)
        header = lines[0].split(";")
        rows = [line.split(";") for line in lines[1:]]
        out = ["## Investigación de keywords (SEMrush)\n", f"Tema: {phrase}\n", "| Keyword | Volumen | CPC | Competencia |", "|---------|--------|-----|-------------|"]
        for r in rows:
            if len(r) >= 4:
                out.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
            elif len(r) == 1:
                out.append(f"| {r[0]} | - | - | - |")
        return "\n".join(out)

    def _read_csv(self, query: str) -> str:
        """Lee keywords de CSV. Path: knowledge/keywords.csv o KEYWORDS_CSV env."""
        base = Path.cwd()
        csv_path = os.getenv("KEYWORDS_CSV", "knowledge/keywords.csv")
        path = Path(csv_path) if Path(csv_path).is_absolute() else base / csv_path
        if not path.is_file():
            return (
                f"No hay CSV de keywords en {path}. Crea knowledge/keywords.csv con columnas: "
                "keyword, volume, cpc, competition (opcional)."
            )

        rows: list[dict[str, str]] = []
        all_rows: list[dict[str, str]] = []
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f, skipinitialspace=True)
                raw = list(reader)
                fieldnames = reader.fieldnames or []
                fn_lower = [c.lower() for c in fieldnames]
                key_col = "keyword" if "keyword" in fn_lower else (fieldnames[0] if fieldnames else "keyword")
                for col in fieldnames:
                    if "key" in col.lower() or "term" in col.lower():
                        key_col = col
                        break
                for row in raw:
                    key = (row.get(key_col) or (list(row.values())[0] if row else "") or "").strip()
                    if not key:
                        continue
                    all_rows.append(row)
                    q = query.lower()
                    if not q or q in key.lower():
                        rows.append(row)
        except Exception as e:
            return f"Error leyendo CSV {path}: {e}"

        if not rows:
            rows = all_rows
        if not rows:
            return (
                f"No hay keywords en {path}. Añade filas con keyword, volume, cpc, competition."
            )

        def _get(r: dict, *keys: str) -> str:
            for k in keys:
                v = r.get(k)
                if v is not None and str(v).strip():
                    return str(v).strip()
            return "-"

        out = ["## Investigación de keywords (CSV)\n", f"Tema: {query}\n", "| Keyword | Volumen | CPC | Competencia |", "|---------|--------|-----|-------------|"]
        for r in rows:
            kw = (r.get(key_col) or (list(r.values())[0] if r else "") or "").strip() or "-"
            vol = _get(r, "volume", "Volume", "Nq")
            cpc = _get(r, "cpc", "CPC", "Cp")
            co = _get(r, "competition", "Competition", "Co")
            out.append(f"| {kw} | {vol} | {cpc} | {co} |")
        return "\n".join(out)

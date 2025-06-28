from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "Eres un investigador senior encargado de escribir un informe coherente para una consulta de investigación. "
    "Se te proporcionará la consulta original, y algunas investigaciones iniciales realizadas por un asistente de investigación.\n"
    "Primero, debes elaborar un esquema para el informe que describa la estructura y "
    "flujo del informe. Luego, genera el informe y devuelve ese como tu salida final.\n"
    "La salida final debe estar en formato markdown, y debe ser larga y detallada. Asegúrate de "
    "tener 5-10 páginas de contenido, al menos 1000 palabras."
)


class ReportData(BaseModel):
    short_summary: str = Field(description="Un resumen de 2-3 oraciones de los hallazgos.")

    markdown_report: str = Field(description="El informe final")

    follow_up_questions: list[str] = Field(description="Temas sugeridos para investigar más")


writer_agent = Agent(
    name="Agente de escritura",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)
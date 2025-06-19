from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Esquema de entrada para MyCustomTool."""
    argument: str = Field(..., description="Descripción del argumento.")

class MyCustomTool(BaseTool):
    name: str = "Nombre de mi herramienta"
    description: str = (
        "Descripción clara de para qué es útil esta herramienta, tu agente necesitará esta información para usarla."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementación aquí
        return "Este es un ejemplo de salida de una herramienta, ignórelo y continúe."

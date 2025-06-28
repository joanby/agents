#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

requirements = """
Un sistema sencillo de gestión de cuentas para una plataforma de simulación de trading.
El sistema debe permitir a los usuarios crear una cuenta, depositar fondos y retirar fondos.
El sistema debe permitir a los usuarios registrar que han comprado o vendido acciones, proporcionando una cantidad.
El sistema debe calcular el valor total del portafolio del usuario, así como la ganancia o pérdida respecto al depósito inicial.
El sistema debe poder informar las posiciones (holdings) del usuario en cualquier momento.
El sistema debe poder informar la ganancia o pérdida del usuario en cualquier momento.
El sistema debe poder listar las transacciones que el usuario ha realizado a lo largo del tiempo.
El sistema debe evitar que el usuario retire fondos que lo dejen con un saldo negativo, o que compre más 
acciones de las que puede pagar, o que venda acciones que no posee.
El sistema tiene acceso a una función get_share_price(symbol) que devuelve el precio actual de una acción, 
e incluye una implementación de prueba que retorna precios fijos para AAPL, TSLA y GOOGL.
"""
module_name = "accounts.py"
class_name = "Account"


def run():
    """
    Crea la tripulación
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }

    # Create and run the crew
    result = EngineeringTeam().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
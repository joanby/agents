#!/usr/bin/env python
import os
from dotenv import load_dotenv

load_dotenv()  # Esto busca el archivo .env y carga las variables
import sys
import warnings




from datetime import datetime

from finagentic.crew import Finagentic

# Create output directory if it doesn't exist
#os.makedirs('output', exist_ok=True)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'financial_product': 'Subrogación de hipotecas en España',
    }

    try:
        Finagentic().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()

#!/usr/bin/env python
# src/financial_researcher/main.py
import os
from financial_researcher.crew import ResearchCrew

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def run():
    """
    Ejecuta la crew para investigación financiera y creación de informes.
    """
    inputs = {
        'company': 'Tesla'
    }

    # Create and run the crew
    result = ResearchCrew().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== INFORME FINAL ===\n\n")
    print(result.raw)

    print("\n\nEl informe ha sido guardado en output/report.md")

if __name__ == "__main__":
    run()
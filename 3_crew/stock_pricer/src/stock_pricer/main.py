#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from stock_pricer.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Ejecuta la crew para seleccionar la mejor empresa para inversión.
    """
    inputs = {
        'sector': 'Tecnología',
        "current_date": str(datetime.now())
    }

    # Create and run the crew
    result = StockPicker().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== DECISION FINAL ===\n\n")
    print(result.raw)


if __name__ == "__main__":
    run()

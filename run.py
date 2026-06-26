"""Lanzador del juego UNO.

Ejecuta el juego sin necesidad de instalar el paquete:

    python run.py
"""

import os
import sys

# Permite importar el paquete `uno` desde la carpeta src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from uno.main import main

if __name__ == "__main__":
    main()

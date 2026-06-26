"""UNO game launcher.

Run the game without installing the package:

    python run.py
"""

import os
import sys

# Allow importing the `uno` package from the src/ folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from uno.main import main

if __name__ == "__main__":
    main()

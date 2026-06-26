"""Saving and loading the game through serialization (pickle).

This is the main feature added to the project: it allows saving the full
game state to disk and resuming it later.
"""

import pickle
from pathlib import Path

# Project root: src/uno/persistence/storage.py -> go up 3 levels
_ROOT = Path(__file__).resolve().parents[3]
SAVE_FILE = _ROOT / "savegame.dat"


def save_game(game) -> None:
    """Serialize the whole game object into `savegame.dat`."""
    with open(SAVE_FILE, "wb") as f:
        pickle.dump(game, f)


def load_game():
    """Load and return the saved game, or None if missing / corrupt."""
    try:
        with open(SAVE_FILE, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        return None


def game_exists() -> bool:
    """True if there is a saved game on disk."""
    return SAVE_FILE.exists()


def delete_game() -> None:
    """Remove the save file (when the game ends)."""
    if SAVE_FILE.exists():
        SAVE_FILE.unlink()

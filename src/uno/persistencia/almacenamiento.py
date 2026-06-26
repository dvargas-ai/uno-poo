"""Guardado y recuperacion de la partida mediante serializacion (pickle).

Esta es la funcionalidad principal anadida al proyecto: permite guardar el
estado completo del juego en disco y continuarlo mas tarde.
"""

import pickle
from pathlib import Path

# Ruta raiz del proyecto: src/uno/persistencia/almacenamiento.py -> sube 3 niveles
_RAIZ = Path(__file__).resolve().parents[3]
ARCHIVO = _RAIZ / "partida.dat"


def guardar_partida(juego) -> None:
    """Serializa el objeto del juego completo en `partida.dat`."""
    with open(ARCHIVO, "wb") as f:
        pickle.dump(juego, f)


def cargar_partida():
    """Carga y devuelve la partida guardada, o None si no existe / falla."""
    try:
        with open(ARCHIVO, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        return None


def existe_partida() -> bool:
    """True si hay una partida guardada en disco."""
    return ARCHIVO.exists()


def borrar_partida() -> None:
    """Elimina el archivo de partida (al terminar el juego)."""
    if ARCHIVO.exists():
        ARCHIVO.unlink()

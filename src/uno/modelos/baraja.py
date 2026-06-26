"""Mazo de cartas: creación, mezcla y robo."""

import random

from uno.modelos.carta import Carta


class Baraja:
    """Mazo de cartas del juego. Se inicializa y se mezcla al crearse."""

    def __init__(self):
        self.cartas: list[Carta] = []
        self._inicializar()
        random.shuffle(self.cartas)

    def _inicializar(self):
        """Genera todas las cartas del mazo."""
        colores = ["R", "A", "V", "Z"]
        comodines_color = ["^", "&", "+2", "+4"]
        comodines_negro = ["+2", "+4", "%"]

        # Cartas numéricas (0-9 por color)
        for c in colores:
            for i in range(10):
                self.cartas.append(Carta(c, str(i)))

        # Comodines de color (2 de cada)
        for c in colores:
            for v in comodines_color:
                self.cartas.append(Carta(c, v))
                self.cartas.append(Carta(c, v))

        # Comodines negros (2 de cada)
        for v in comodines_negro:
            self.cartas.append(Carta("N", v))
            self.cartas.append(Carta("N", v))

    def esta_vacia(self) -> bool:
        """True si ya no quedan cartas en el mazo."""
        return len(self.cartas) == 0

    def robar(self) -> Carta | None:
        """Saca y devuelve la carta superior, o None si el mazo está vacío."""
        if self.esta_vacia():
            return None
        return self.cartas.pop(0)

    def tamano(self) -> int:
        """Cantidad de cartas restantes en el mazo."""
        return len(self.cartas)

    def mostrar(self):
        """Imprime todas las cartas del mazo (uso de depuración)."""
        print(" ".join(str(c) for c in self.cartas))

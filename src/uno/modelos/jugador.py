"""Jugador del juego (humano o maquina) y su mano de cartas."""

from uno.modelos.carta import Carta


class Jugador:
    """Representa a un jugador y administra su mano de cartas."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.mano: list[Carta] = []

    def agregar_carta(self, carta: Carta | None):
        """Anade una carta a la mano (ignora None, p. ej. mazo vacio)."""
        if carta:
            self.mano.append(carta)

    def jugar_carta(self, indice: int) -> Carta | None:
        """Quita y devuelve la carta en `indice`, o None si es invalido."""
        if 0 <= indice < len(self.mano):
            return self.mano.pop(indice)
        return None

    def tamano_mano(self) -> int:
        """Cantidad de cartas en la mano."""
        return len(self.mano)

    def mostrar_mano(self):
        """Imprime la mano con indices para que el humano elija."""
        print(f"Mano de {self.nombre}:")
        for i, carta in enumerate(self.mano):
            print(f"  [{i}] {carta}")

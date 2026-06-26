"""Representacion de una carta del juego UNO."""

from dataclasses import dataclass


@dataclass
class Carta:
    """Una carta del mazo.

    Atributos:
        color: R (rojo), A (amarillo), V (verde), Z (azul) o N (negro/comodin).
        valor: '0'-'9' para cartas numericas, o un comodin:
            '^' saltar, '&' reversa, '%' cambio de color, '+2', '+4'.
    """

    color: str
    valor: str

    def es_numero(self) -> bool:
        """Devuelve True si la carta es numerica (0-9)."""
        return len(self.valor) == 1 and self.valor.isdigit()

    def es_comodin(self) -> bool:
        """Devuelve True si la carta es un comodin (no numerica)."""
        return not self.es_numero()

    def __str__(self) -> str:
        return f"{self.color}{self.valor}"

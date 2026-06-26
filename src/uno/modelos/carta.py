"""Representación de una carta del juego UNO."""

from dataclasses import dataclass


@dataclass
class Carta:
    """Una carta del mazo.

    Atributos:
        color: R (rojo), A (amarillo), V (verde), Z (azul) o N (negro/comodín).
        valor: '0'-'9' para cartas numéricas, o un comodín:
            '^' saltar, '&' reversa, '%' cambio de color, '+2', '+4'.
    """

    color: str
    valor: str

    def es_numero(self) -> bool:
        """Devuelve True si la carta es numérica (0-9)."""
        return len(self.valor) == 1 and self.valor.isdigit()

    def es_comodin(self) -> bool:
        """Devuelve True si la carta es un comodín (no numérica)."""
        return not self.es_numero()

    def __str__(self) -> str:
        return f"{self.color}{self.valor}"

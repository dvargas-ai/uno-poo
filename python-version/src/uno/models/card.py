"""Representation of a single UNO card."""

from dataclasses import dataclass


@dataclass
class Card:
    """A card from the deck.

    Attributes:
        color: R (red), Y (yellow), G (green), B (blue) or W (black/wild).
        value: '0'-'9' for number cards, or a wild card:
            '^' skip, '&' reverse, '%' color change, '+2', '+4'.
    """

    color: str
    value: str

    def is_number(self) -> bool:
        """Return True if the card is a number card (0-9)."""
        return len(self.value) == 1 and self.value.isdigit()

    def is_wild(self) -> bool:
        """Return True if the card is a wild card (not a number)."""
        return not self.is_number()

    def __str__(self) -> str:
        return f"{self.color}{self.value}"

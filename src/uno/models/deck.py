"""The deck of cards: creation, shuffling and drawing."""

import random

from uno.models.card import Card


class Deck:
    """The game deck. It is built and shuffled when created."""

    def __init__(self):
        self.cards: list[Card] = []
        self._initialize()
        random.shuffle(self.cards)

    def _initialize(self):
        """Generate every card in the deck."""
        colors = ["R", "Y", "G", "B"]
        colored_wilds = ["^", "&", "+2", "+4"]
        black_wilds = ["+2", "+4", "%"]

        # Number cards (0-9 per color)
        for c in colors:
            for i in range(10):
                self.cards.append(Card(c, str(i)))

        # Colored wild cards (2 of each)
        for c in colors:
            for v in colored_wilds:
                self.cards.append(Card(c, v))
                self.cards.append(Card(c, v))

        # Black wild cards (2 of each)
        for v in black_wilds:
            self.cards.append(Card("W", v))
            self.cards.append(Card("W", v))

    def is_empty(self) -> bool:
        """True if there are no cards left in the deck."""
        return len(self.cards) == 0

    def draw(self) -> Card | None:
        """Remove and return the top card, or None if the deck is empty."""
        if self.is_empty():
            return None
        return self.cards.pop(0)

    def size(self) -> int:
        """Number of cards remaining in the deck."""
        return len(self.cards)

    def show(self):
        """Print every card in the deck (debugging helper)."""
        print(" ".join(str(c) for c in self.cards))

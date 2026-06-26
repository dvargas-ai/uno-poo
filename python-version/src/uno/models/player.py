"""Game player (human or computer) and their hand of cards."""

from uno.models.card import Card


class Player:
    """Represents a player and manages their hand of cards."""

    def __init__(self, name: str):
        self.name = name
        self.hand: list[Card] = []

    def add_card(self, card: Card | None):
        """Add a card to the hand (ignores None, e.g. an empty deck)."""
        if card:
            self.hand.append(card)

    def play_card(self, index: int) -> Card | None:
        """Remove and return the card at `index`, or None if invalid."""
        if 0 <= index < len(self.hand):
            return self.hand.pop(index)
        return None

    def hand_size(self) -> int:
        """Number of cards in the hand."""
        return len(self.hand)

    def show_hand(self):
        """Print the hand with indices so the human can choose."""
        print(f"{self.name}'s hand:")
        for i, card in enumerate(self.hand):
            print(f"  [{i}] {card}")

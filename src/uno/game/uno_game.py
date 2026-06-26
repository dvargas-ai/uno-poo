"""Core UNO game logic: turns, rules and card effects."""

from uno.models.card import Card
from uno.models.deck import Deck
from uno.models.player import Player
from uno.persistence.storage import delete_game, save_game


class UnoGame:
    """Controls a game between the human player and the computer."""

    def __init__(self):
        self.deck = Deck()
        self.player1 = Player("Player 1")
        self.player2 = Player("Computer")
        self.table_card: Card | None = None
        self.current_color: str = ""
        self.skip_p1 = False
        self.skip_p2 = False
        self.played_cards: list[Card] = []

        self._deal_cards()
        self._initialize_table()

    def _deal_cards(self):
        """Deal 7 cards to each player."""
        for _ in range(7):
            self.player1.add_card(self.deck.draw())
            self.player2.add_card(self.deck.draw())

    def _initialize_table(self):
        """Place the first card on the table (must be a number card)."""
        while True:
            card = self.deck.draw()
            if card and card.is_number():
                self.table_card = card
                self.current_color = card.color
                self.played_cards.append(card)
                break

    def _has_play(self, player: Player) -> bool:
        """True if the player has at least one valid card to play."""
        for card in player.hand:
            if self._is_valid_play(card):
                return True
        return False

    def play(self):
        """Main game loop until someone runs out of cards."""
        finished = False

        while not finished:
            self._show_state()

            # Human player's turn
            if self.skip_p1:
                print("Player 1 loses their turn.")
                self.skip_p1 = False
            else:
                finished = self._human_turn(self.player1)
                save_game(self)
                if finished:
                    break

            if self.player1.hand_size() == 0 or self.player2.hand_size() == 0:
                break

            print("\n--- COMPUTER TURN ---\n")

            # Computer's turn
            if self.skip_p2:
                print("The computer loses its turn.")
                self.skip_p2 = False
            else:
                finished = self._computer_turn(self.player2)
                save_game(self)
                if finished:
                    break

            print("\n-----------------------------\n")

        self._end_game()

    def _show_state(self):
        """Print the current state of the table and the hands."""
        print(f"\nCard on table: {self.table_card} | Current color: {self.current_color}")
        print("Played cards:", " ".join(str(c) for c in self.played_cards))

        print()
        self.player1.show_hand()
        print()
        print("Computer's hand:")
        for c in self.player2.hand:
            print(c, end="  ")
        print()

        print(f"\nCards in deck: {self.deck.size()}\n")

    def _is_valid_play(self, card: Card) -> bool:
        """Apply the UNO rules to validate whether a card can be played."""
        top_is_wild = self.table_card.is_wild()

        if top_is_wild and card.is_wild():
            return False

        if card.is_number():
            return card.color == self.current_color or card.value == self.table_card.value
        else:
            if card.color != "W":
                return card.color == self.current_color and not top_is_wild
            else:
                return not top_is_wild

    def _human_turn(self, player: Player) -> bool:
        """Handle the human's turn. Return True if they won."""
        if not self._has_play(player):
            print("You have no valid card. You draw and lose your turn.")
            player.add_card(self.deck.draw())
            return False

        while True:
            try:
                i = int(input("Index of card to play: "))
                card = player.hand[i]
                if not self._is_valid_play(card):
                    print("Invalid card.")
                    continue
                break
            except (ValueError, IndexError):
                print("Invalid input.")

        played = player.play_card(i)
        print(f"You play {played}")
        self._process_play(played, player)

        if player.hand_size() == 1:
            print("UNO!!!")

        return player.hand_size() == 0

    def _computer_turn(self, player: Player) -> bool:
        """Handle the computer's turn. Return True if it won."""
        for i, c in enumerate(player.hand):
            if self._is_valid_play(c):
                played = player.play_card(i)
                print(f"Computer plays {played}")
                self._process_play(played, player)
                break
        else:
            print("Computer draws a card.")
            player.add_card(self.deck.draw())

        if player.hand_size() == 1:
            print("UNO!!! (Computer)")

        return player.hand_size() == 0

    def _process_play(self, card: Card, player: Player):
        """Place the card on the table, set the color and apply its effect."""
        self.table_card = card
        self.played_cards.append(card)

        if card.color == "W":
            if player == self.player1:
                self.current_color = self._ask_color()
            else:
                self.current_color = self._computer_color()
                print("Computer changes color to:", self.current_color)
        else:
            self.current_color = card.color

        self._apply_effect(card, player)

    def _apply_effect(self, card: Card, player: Player):
        """Apply the skip/draw effect based on the card value."""
        other = self.player2 if player == self.player1 else self.player1
        v = card.value

        if v in ["^", "&"]:
            if player == self.player1:
                self.skip_p2 = True
            else:
                self.skip_p1 = True

        elif v == "+2":
            print("The other player draws 2.")
            for _ in range(2):
                other.add_card(self.deck.draw())
            if player == self.player1:
                self.skip_p2 = True
            else:
                self.skip_p1 = True

        elif v == "+4":
            print("The other player draws 4.")
            for _ in range(4):
                other.add_card(self.deck.draw())
            if player == self.player1:
                self.skip_p2 = True
            else:
                self.skip_p1 = True

    def _ask_color(self) -> str:
        """Ask the human to choose a color after playing a wild card."""
        while True:
            c = input("Choose color (R,Y,G,B): ").upper()
            if c in ["R", "Y", "G", "B"]:
                return c

    def _computer_color(self) -> str:
        """The computer picks the color it holds the most cards of."""
        counts = {"R": 0, "Y": 0, "G": 0, "B": 0}
        for c in self.player2.hand:
            if c.color in counts:
                counts[c.color] += 1
        return max(counts, key=counts.get)

    def _end_game(self):
        """Announce the winner and delete the saved game."""
        print("\n=== GAME OVER ===")
        if self.player1.hand_size() == 0:
            print("YOU WIN!")
        else:
            print("THE COMPUTER WINS")

        delete_game()

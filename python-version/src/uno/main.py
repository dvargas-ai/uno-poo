"""Entry point of the UNO game.

Offers to resume a saved game or start a new one.
"""

from uno.game.uno_game import UnoGame
from uno.persistence.storage import game_exists, load_game


def main():
    if game_exists():
        choice = input("There is a saved game. Continue? (Y/N): ").strip().upper()
        if choice == "Y":
            game = load_game()
            if game is not None:
                game.play()
                return
            print("The saved game could not be loaded. A new one will start.")

    game = UnoGame()
    game.play()


if __name__ == "__main__":
    main()

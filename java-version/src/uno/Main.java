package uno;

import uno.game.UnoGame;

/**
 * Entry point of the UNO game.
 *
 * First-midterm version: starts a single game. There is no save/resume,
 * so running the program again always begins a brand new game.
 */
public class Main {

    public static void main(String[] args) {
        UnoGame game = new UnoGame();
        game.play();
    }
}

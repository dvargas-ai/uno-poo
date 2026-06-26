package uno.game;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

import uno.models.Card;
import uno.models.Deck;
import uno.models.Player;

/**
 * Core UNO game logic: turns, rules and card effects.
 *
 * This is the first-midterm version: a single game per run, with no
 * save/resume feature.
 */
public class UnoGame {

    private final Deck deck;
    private final Player player1;
    private final Player player2;
    private Card tableCard;
    private String currentColor;
    private boolean skipP1;
    private boolean skipP2;
    private final List<Card> playedCards;
    private final Scanner scanner;

    public UnoGame() {
        deck = new Deck();
        player1 = new Player("Player 1");
        player2 = new Player("Computer");
        tableCard = null;
        currentColor = "";
        skipP1 = false;
        skipP2 = false;
        playedCards = new ArrayList<>();
        scanner = new Scanner(System.in);

        dealCards();
        initializeTable();
    }

    /** Deal 7 cards to each player. */
    private void dealCards() {
        for (int i = 0; i < 7; i++) {
            player1.addCard(deck.draw());
            player2.addCard(deck.draw());
        }
    }

    /** Place the first card on the table (must be a number card). */
    private void initializeTable() {
        while (true) {
            Card card = deck.draw();
            if (card != null && card.isNumber()) {
                tableCard = card;
                currentColor = card.getColor();
                playedCards.add(card);
                break;
            }
        }
    }

    /** True if the player has at least one valid card to play. */
    private boolean hasPlay(Player player) {
        for (Card card : player.getHand()) {
            if (isValidPlay(card)) {
                return true;
            }
        }
        return false;
    }

    /** Main game loop until someone runs out of cards. */
    public void play() {
        boolean finished = false;

        while (!finished) {
            showState();

            // Human player's turn
            if (skipP1) {
                System.out.println("Player 1 loses their turn.");
                skipP1 = false;
            } else {
                finished = humanTurn(player1);
                if (finished) {
                    break;
                }
            }

            if (player1.handSize() == 0 || player2.handSize() == 0) {
                break;
            }

            System.out.println("\n--- COMPUTER TURN ---\n");

            // Computer's turn
            if (skipP2) {
                System.out.println("The computer loses its turn.");
                skipP2 = false;
            } else {
                finished = computerTurn(player2);
                if (finished) {
                    break;
                }
            }

            System.out.println("\n-----------------------------\n");
        }

        endGame();
    }

    /** Print the current state of the table and the hands. */
    private void showState() {
        System.out.println("\nCard on table: " + tableCard + " | Current color: " + currentColor);

        StringBuilder played = new StringBuilder();
        for (Card c : playedCards) {
            played.append(c).append(" ");
        }
        System.out.println("Played cards: " + played.toString().trim());

        System.out.println();
        player1.showHand();
        System.out.println();
        System.out.println("Computer's hand:");
        StringBuilder hand = new StringBuilder();
        for (Card c : player2.getHand()) {
            hand.append(c).append("  ");
        }
        System.out.println(hand.toString());

        System.out.println("\nCards in deck: " + deck.size() + "\n");
    }

    /** Apply the UNO rules to validate whether a card can be played. */
    private boolean isValidPlay(Card card) {
        boolean topIsWild = tableCard.isWild();

        if (topIsWild && card.isWild()) {
            return false;
        }

        if (card.isNumber()) {
            return card.getColor().equals(currentColor)
                    || card.getValue().equals(tableCard.getValue());
        } else {
            if (!card.getColor().equals("W")) {
                return card.getColor().equals(currentColor) && !topIsWild;
            } else {
                return !topIsWild;
            }
        }
    }

    /** Handle the human's turn. Return true if they won. */
    private boolean humanTurn(Player player) {
        if (!hasPlay(player)) {
            System.out.println("You have no valid card. You draw and lose your turn.");
            player.addCard(deck.draw());
            return false;
        }

        int i;
        while (true) {
            System.out.print("Index of card to play: ");
            try {
                i = Integer.parseInt(scanner.nextLine().trim());
                Card card = player.getHand().get(i);
                if (!isValidPlay(card)) {
                    System.out.println("Invalid card.");
                    continue;
                }
                break;
            } catch (NumberFormatException | IndexOutOfBoundsException e) {
                System.out.println("Invalid input.");
            }
        }

        Card played = player.playCard(i);
        System.out.println("You play " + played);
        processPlay(played, player);

        if (player.handSize() == 1) {
            System.out.println("UNO!!!");
        }

        return player.handSize() == 0;
    }

    /** Handle the computer's turn. Return true if it won. */
    private boolean computerTurn(Player player) {
        boolean playedSomething = false;
        for (int i = 0; i < player.getHand().size(); i++) {
            if (isValidPlay(player.getHand().get(i))) {
                Card played = player.playCard(i);
                System.out.println("Computer plays " + played);
                processPlay(played, player);
                playedSomething = true;
                break;
            }
        }
        if (!playedSomething) {
            System.out.println("Computer draws a card.");
            player.addCard(deck.draw());
        }

        if (player.handSize() == 1) {
            System.out.println("UNO!!! (Computer)");
        }

        return player.handSize() == 0;
    }

    /** Place the card on the table, set the color and apply its effect. */
    private void processPlay(Card card, Player player) {
        tableCard = card;
        playedCards.add(card);

        if (card.getColor().equals("W")) {
            if (player == player1) {
                currentColor = askColor();
            } else {
                currentColor = computerColor();
                System.out.println("Computer changes color to: " + currentColor);
            }
        } else {
            currentColor = card.getColor();
        }

        applyEffect(card, player);
    }

    /** Apply the skip/draw effect based on the card value. */
    private void applyEffect(Card card, Player player) {
        Player other = (player == player1) ? player2 : player1;
        String v = card.getValue();

        if (v.equals("^") || v.equals("&")) {
            if (player == player1) {
                skipP2 = true;
            } else {
                skipP1 = true;
            }
        } else if (v.equals("+2")) {
            System.out.println("The other player draws 2.");
            for (int k = 0; k < 2; k++) {
                other.addCard(deck.draw());
            }
            if (player == player1) {
                skipP2 = true;
            } else {
                skipP1 = true;
            }
        } else if (v.equals("+4")) {
            System.out.println("The other player draws 4.");
            for (int k = 0; k < 4; k++) {
                other.addCard(deck.draw());
            }
            if (player == player1) {
                skipP2 = true;
            } else {
                skipP1 = true;
            }
        }
    }

    /** Ask the human to choose a color after playing a wild card. */
    private String askColor() {
        while (true) {
            System.out.print("Choose color (R,Y,G,B): ");
            String c = scanner.nextLine().trim().toUpperCase();
            if (c.equals("R") || c.equals("Y") || c.equals("G") || c.equals("B")) {
                return c;
            }
        }
    }

    /** The computer picks the color it holds the most cards of. */
    private String computerColor() {
        Map<String, Integer> counts = new LinkedHashMap<>();
        counts.put("R", 0);
        counts.put("Y", 0);
        counts.put("G", 0);
        counts.put("B", 0);

        for (Card c : player2.getHand()) {
            if (counts.containsKey(c.getColor())) {
                counts.put(c.getColor(), counts.get(c.getColor()) + 1);
            }
        }

        String best = "R";
        int bestCount = -1;
        for (Map.Entry<String, Integer> e : counts.entrySet()) {
            if (e.getValue() > bestCount) {
                bestCount = e.getValue();
                best = e.getKey();
            }
        }
        return best;
    }

    /** Announce the winner. */
    private void endGame() {
        System.out.println("\n=== GAME OVER ===");
        if (player1.handSize() == 0) {
            System.out.println("YOU WIN!");
        } else {
            System.out.println("THE COMPUTER WINS");
        }
    }
}

package uno.models;

import java.util.ArrayList;
import java.util.List;

/** A player (human or computer) and their hand of cards. */
public class Player {

    private final String name;
    private final List<Card> hand = new ArrayList<>();

    public Player(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public List<Card> getHand() {
        return hand;
    }

    /** Add a card to the hand (ignores null, e.g. an empty deck). */
    public void addCard(Card card) {
        if (card != null) {
            hand.add(card);
        }
    }

    /** Remove and return the card at index, or null if invalid. */
    public Card playCard(int index) {
        if (index >= 0 && index < hand.size()) {
            return hand.remove(index);
        }
        return null;
    }

    /** Number of cards in the hand. */
    public int handSize() {
        return hand.size();
    }

    /** Print the hand with indices so the human can choose. */
    public void showHand() {
        System.out.println(name + "'s hand:");
        for (int i = 0; i < hand.size(); i++) {
            System.out.println("  [" + i + "] " + hand.get(i));
        }
    }
}

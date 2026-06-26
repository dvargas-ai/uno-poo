package uno.models;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** The deck of cards: built and shuffled when created. */
public class Deck {

    private final List<Card> cards = new ArrayList<>();

    public Deck() {
        initialize();
        Collections.shuffle(cards);
    }

    /** Generate every card in the deck. */
    private void initialize() {
        String[] colors = {"R", "Y", "G", "B"};
        String[] coloredWilds = {"^", "&", "+2", "+4"};
        String[] blackWilds = {"+2", "+4", "%"};

        // Number cards (0-9 per color)
        for (String c : colors) {
            for (int i = 0; i < 10; i++) {
                cards.add(new Card(c, String.valueOf(i)));
            }
        }

        // Colored wild cards (2 of each)
        for (String c : colors) {
            for (String v : coloredWilds) {
                cards.add(new Card(c, v));
                cards.add(new Card(c, v));
            }
        }

        // Black wild cards (2 of each)
        for (String v : blackWilds) {
            cards.add(new Card("W", v));
            cards.add(new Card("W", v));
        }
    }

    /** True if there are no cards left in the deck. */
    public boolean isEmpty() {
        return cards.isEmpty();
    }

    /** Remove and return the top card, or null if the deck is empty. */
    public Card draw() {
        if (isEmpty()) {
            return null;
        }
        return cards.remove(0);
    }

    /** Number of cards remaining in the deck. */
    public int size() {
        return cards.size();
    }

    /** Print every card in the deck (debugging helper). */
    public void show() {
        StringBuilder sb = new StringBuilder();
        for (Card c : cards) {
            sb.append(c).append(" ");
        }
        System.out.println(sb.toString().trim());
    }
}

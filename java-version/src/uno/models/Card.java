package uno.models;

/**
 * Representation of a single UNO card.
 *
 * color: R (red), Y (yellow), G (green), B (blue) or W (black/wild).
 * value: "0"-"9" for number cards, or a wild card:
 *        "^" skip, "&" reverse, "%" color change, "+2", "+4".
 */
public class Card {

    private final String color;
    private final String value;

    public Card(String color, String value) {
        this.color = color;
        this.value = value;
    }

    public String getColor() {
        return color;
    }

    public String getValue() {
        return value;
    }

    /** Return true if the card is a number card (0-9). */
    public boolean isNumber() {
        return value.length() == 1 && Character.isDigit(value.charAt(0));
    }

    /** Return true if the card is a wild card (not a number). */
    public boolean isWild() {
        return !isNumber();
    }

    @Override
    public String toString() {
        return color + value;
    }
}

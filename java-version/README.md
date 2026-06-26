# UNO — Java version (1st midterm)

Original object-oriented implementation of the UNO game in Java.
This is the **first-midterm** version: it plays a **single game per run** and
has **no save/resume feature** (that was added later in the Python version).

See the [main README](../README.md) for the full project overview, UML diagram
and the Java → Python comparison.

## Requirements

- JDK 17 or higher (`javac` and `java` on your PATH).

## Compile and run

```bash
javac -d out src/uno/Main.java src/uno/models/*.java src/uno/game/*.java
java -cp out uno.Main
```

## Structure

```
src/uno/
├── Main.java              # Entry point
├── models/
│   ├── Card.java
│   ├── Deck.java
│   └── Player.java
└── game/
    └── UnoGame.java       # Game logic, turns and rules
```

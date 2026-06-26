# Object-oriented design

This document describes the project's classes and how they relate.

## Classes

### `Card` (`src/uno/models/card.py`)
Models a card with `color` and `value`. Implemented as a `dataclass`.
- `is_number()` / `is_wild()`: classify the card.

### `Deck` (`src/uno/models/deck.py`)
Deck of cards. Built with all cards and shuffled automatically.
- `draw()`: hands out the top card.
- `is_empty()`, `size()`.

### `Player` (`src/uno/models/player.py`)
Represents a player (human or computer) and their hand.
- `add_card()`, `play_card()`, `show_hand()`.

### `UnoGame` (`src/uno/game/uno_game.py`)
Controls the whole game: dealing, turns, play validation, card effects (skip,
+2, +4, color change) and game over.

### Persistence (`src/uno/persistence/storage.py`)
Functions to save/load the game state with `pickle`:
`save_game`, `load_game`, `game_exists`, `delete_game`.

## Relationships (composition)

```
UnoGame
 |-- Deck             (1)
 |     |-- Card       (*)
 |-- Player           (2)
       |-- Card       (hand, *)
```

`UnoGame` relies on the persistence module to save its state after each turn.

## Game flow

1. `main.py` checks for a saved game and offers to resume it.
2. `UnoGame` deals the cards and places the starting card on the table.
3. Turns alternate (human <-> computer) until someone runs out of cards. After
   each turn the game is saved.
4. When it finishes, the winner is announced and the save file is deleted.

# UNO — Python version (2nd midterm)

The UNO game migrated from Java to Python, **plus a new save/resume feature**.
This is the **second-midterm** version: the game is saved automatically after
each turn, so a game in progress can be continued later.

See the [main README](../README.md) for the full project overview, UML diagram
and the Java → Python comparison.

## Requirements

- Python 3.10 or higher (standard library only, no external dependencies).

## Run

```bash
python run.py
```

## How to play

- You play against the **computer**. Each player starts with **7 cards**.
- On your turn your hand is shown numbered; type the **index** of the card to
  play.
- A card is valid if it **matches the color or the number/symbol** of the card
  on the table.
- If you have no valid play, you draw a card and lose your turn.
- The first player to run **out of cards** wins.

## Saving the game

The game is saved automatically after every turn to `savegame.dat` using the
`pickle` module. When the game starts, if a saved game exists, you are offered
to resume it. When the game ends, the file is deleted automatically.

## Structure

```
run.py                    # Launcher (python run.py)
docs/STRUCTURE.md         # Object-oriented design explanation
src/uno/
├── main.py               # Start menu: new game or resume
├── models/               # card.py, deck.py, player.py
├── game/                 # uno_game.py
└── persistence/          # storage.py (save/load)
```

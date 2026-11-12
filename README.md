# Azul AI agent

A game engine and an adversarial-search agent for the board game Azul, written in Python for a student AI competition at the University of Montenegro, where it took 1st place.

## How it works

**Game engine** (`azul.py`)

- Represents the game state (factories, each player's board and score) as a dictionary.
- `get_actions` lists every legal move as (factory, tile colour, destination row), and `get_successor` applies a move to a copy of the state.
- Implements end-of-round scoring, including Azul's adjacency rule for wall tiles, and refills the factories.

**Agents** (`agents.py`)

- `AlphaBeta`: minimax search with alpha-beta pruning to a fixed depth.
- `AlphaBetaVremenski` ("timed"): iterative deepening with alpha-beta pruning. It searches depth 1, then 2, then 3 and so on, and stops when a time limit (9 s by default) runs out, keeping the best move from the last fully completed depth. This plays as deep as the time allows on every move.

## Run

```sh
python main.py
```

You play against the bot in the terminal. On your turn, enter the factory, the tile colour (`W`, `R`, `Y`, `K`, `B`) and the destination row, one per line. `main.py` fixes the tiles for the first round, so games start the same way every time.

## Files

| File | Contents |
| --- | --- |
| `azul.py` | Game rules, state transitions and scoring |
| `agents.py` | Game loop and the two search agents |
| `main.py` | Starts a game against the timed agent |
| `130634-Domaci01_2024.pdf` | Competition assignment (in Montenegrin) |

Code identifiers and comments are in Montenegrin.

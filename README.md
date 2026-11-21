# Owl Town RPG

The original Python text RPG, with a shared game engine that can later power a
browser interface. The terminal game remains playable. No third-party Python
packages are required. Python 3.10 or newer is supported.

## Play in the terminal

From the repository directory:

```sh
python main.py
```

Choose a character with `1` through `5`. Type `help` for commands. The original
first-letter shortcuts work: `h`, `s`, `b`, `e`, `a`, `r`, `u`, `f`, and `q`.
`use special` is the full special-attack command. Commands ignore case and extra
whitespace. Additional unrelated words are rejected rather than ignored.

Library visits ask for a book on the next turn. Choose `1` through `5`, or `0` to
leave without a book. Invalid choices repeat the prompt. `quit` or `q` works at
any prompt. End-of-input and Ctrl+C also end the terminal session.

## Architecture

- `scripts/classes.py` retains the original character hierarchy, combat,
  exploration, books, and story data. Rules emit messages to a collector and use
  an injected random-number generator.
- `scripts/engine.py` owns one session, routes commands and pending choices, and
  resolves boss progression, victory, defeat, and quitting.
- `main.py` renders messages and handles terminal input and the introduction's
  delay. The rules do not read input, print, sleep, or exit the process.
- `tests/` protects original working rules, the bug fixes, and terminal sessions.

To drive the same Python game from another interface:

```python
import random
from scripts.engine import Game

game = Game(rng=random.Random(42))  # Omit rng for a normal random game.
intro = game.start()
selection = game.submit("5")
turn = game.submit("explore")
```

Each result is a fresh, JSON-compatible dictionary:

- `messages`: the messages produced by this turn, in display order.
- `phase`: `character_selection`, `exploration`, `book_selection`, `combat`,
  `boss_combat`, `won`, `lost`, or `quit`.
- `prompt`: the next input prompt, or `None` when finished.
- `choices`: command or menu values and display labels. Commands may have
  different consequences depending on the phase; the engine validates them.
- `state`: a snapshot containing player statistics, books, and the active enemy.
- `finished`: whether the session has ended.

Call `start()` before `submit()`. Calling `start()` again does not reset the
session or repeat the introduction. Submissions after an ending do not change
the game. To restart, construct a new `Game`. A state snapshot is for display;
it is not yet a save-game format. Adapters should call the engine sequentially.

## Preservation and corrections

The story text, characters, starting statistics, exploration probabilities,
damage formula, author-reading priority, and first-letter commands are retained.
Parker uses the special name from the original playable introduction:
`REKRAP ASTRAL PLANE!`.

Knowledge still acts as both health and progression. Reaching 16 current
knowledge starts the boss encounter once the player is out of ordinary combat.
Ordinary victories increase current and maximum knowledge; special victories
still increase only current knowledge. This can exceed the maximum, as in the
original game. Balancing these rules is separate from extracting the engine.

The cleanup corrects these defects:

- Character and book choices are validated strings; input is never evaluated as
  Python code.
- Zero knowledge ends the session immediately, including during the boss fight.
- Boss victory requires defeating the boss. Successful escape returns to
  exploration, and the next `explore` resumes that same boss with its remaining
  knowledge. Escape no longer triggers the win screen.
- Special attacks actually reduce the enemy to zero and charges cannot become
  negative. Both attack types share encounter cleanup while retaining their
  original different rewards.
- Reading an empty backpack is safe and awards no knowledge.
- Inventory contains actual books, without placeholder slots. All books are
  displayed, duplicate copies remain usable, and the count is derived from the
  inventory. No six-book capacity rule is introduced; the old pickup code did
  not enforce one.
- Book data is immutable, so sessions can safely share the story constants.

## Tests

```sh
python -B -m unittest discover -s tests -v
```

The initial seven characterization tests were first run against the unmodified
game. After extraction, those assertions use collected messages instead of
capturing standard output. Scripted random rolls test individual branches and
complete playthroughs. Seeded replay checks all random choices use the same
session generator. Terminal tests exercise selection, library input, victory,
defeat, restart, and interrupted input through the real engine.

GitHub Actions runs the suite on Linux and Windows with Python 3.10 and 3.14.
This stage adds no browser interface, hosting, DNS changes, or LLM dependency.
The engine interface is the foundation for a later Pyodide browser adapter and
GitHub Pages deployment.

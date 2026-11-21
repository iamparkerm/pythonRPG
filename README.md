# Owl Town RPG

A Python text RPG for learning and playing with friends. The original story and
terminal game are preserved. Use Python 3.12 on Windows; no extra packages needed.

## Play

Open PowerShell in the repository folder:

```powershell
python main.py
```

Choose a character with 1–5. Type `help` for commands. First-letter shortcuts
work: h, s, b, e, a, r, u, f, q. The full special command is `use special`.
In the library, pick a book with 1–5 or leave with 0. Type q to quit.

## Read the code

- `scripts/classes.py`: characters, combat, exploration, books, and story data.
  Rules collect messages instead of printing them.
- `scripts/engine.py`: one game session. Tracks which part of the game you're
  in and handles one command or menu choice at a time.
- `main.py`: the terminal loop. It asks for input and prints the messages.
- `tests/`: original working rules, the known bugs, and a complete playthrough.

The main change is separating *what happens* from *how it is displayed*. The
terminal uses the engine now; a browser can use the same Python rules later.

```python
from scripts.engine import Game

game = Game()
intro = game.start()          # List of introduction messages
messages = game.submit("5")  # Select Parker
messages = game.submit("e")  # Explore
```

`start()` returns the introduction. `submit(text)` returns that turn's messages.
`game.phase` tells you whether you're choosing, exploring, fighting, or finished.
`game.prompt` is the next input prompt; `game.finished` ends the loop.
Create another `Game()` to start over.

## What was fixed

- Menu choices no longer execute Python expressions.
- Empty backpacks display correctly, and reading without books is safe.
- All collected books are shown; the book count comes from the inventory.
- Specials actually defeat the enemy, and charges stop at zero.
- Dying during the boss fight ends the game.
- Escaping the boss no longer wins. The next exploration resumes the same boss.

Knowledge still serves as both health and progression. Ordinary wins increase
current and maximum knowledge; special wins increase only current knowledge.
These original balance rules are unchanged. Parker keeps the special name from
the original introduction. Book reading keeps its original author priority.

## Run the tests

```powershell
python -B -m unittest discover -s tests -v
```

The first seven tests were checked against the original game before extraction.
The remaining tests cover the listed fixes and normal play. One Windows check
runs the same command on GitHub when code changes.

Browser hosting and LLM agents come later.

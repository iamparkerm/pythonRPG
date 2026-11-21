"""Terminal interface for Owl Town RPG. Run with: python main.py"""

import time

from scripts.engine import Game


def main():
    game = Game()
    intro = game.start()
    print(intro[0])
    time.sleep(2)
    print(intro[1])

    while not game.finished:
        try:
            text = input(game.prompt)
        except (EOFError, KeyboardInterrupt):
            text = 'quit'
        for message in game.submit(text):
            print(message)


if __name__ == '__main__':
    main()

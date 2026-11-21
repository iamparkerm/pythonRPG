"""Terminal adapter for Owl Town RPG. Run with: python main.py"""

import time

from scripts.engine import Game


def main(read=input, write=print, pause=time.sleep):
    game = Game()
    result = game.start()
    for index, message in enumerate(result['messages']):
        write(message)
        if index == 0:
            pause(2)

    while not result['finished']:
        try:
            text = read(result['prompt'])
        except (EOFError, KeyboardInterrupt):
            text = 'quit'
        result = game.submit(text)
        for message in result['messages']:
            write(message)
    return game


if __name__ == '__main__':
    main()

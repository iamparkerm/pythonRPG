"""Make sure the terminal entry point still uses the game correctly."""

import unittest
from unittest.mock import patch

import main
from scripts.engine import Game


class TerminalTests(unittest.TestCase):
    def test_select_read_show_stats_and_quit(self):
        with patch('builtins.input', side_effect=['5', 'b', 'r', 's', 'q']), \
             patch('builtins.print') as output, patch('main.time.sleep'):
            main.main()
        output.assert_any_call('your trusty journal')
        output.assert_any_call("Parker's knowledge: 8/8 special: 2 book(s): 0")

    def test_terminal_stops_after_defeat(self):
        game = Game()
        with patch('main.Game', return_value=game), \
             patch.object(game.player.rng, 'randint', side_effect=[1, 6, 6, 0, 6, 0]), \
             patch('builtins.input', side_effect=['5', 'e', 'r', 'r']) as read, \
             patch('builtins.print'), patch('main.time.sleep'):
            main.main()
        self.assertEqual(game.phase, 'lost')
        self.assertEqual(read.call_count, 4)


if __name__ == '__main__':
    unittest.main()

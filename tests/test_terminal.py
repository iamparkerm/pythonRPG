"""Exercise the terminal adapter with real engine sessions and scripted input."""

import random
import unittest
from unittest.mock import Mock, patch

import main
from scripts.engine import Game


class TerminalTests(unittest.TestCase):
    def test_scripted_session_keeps_original_intro_and_commands(self):
        read = Mock(side_effect=['', '5', 'b', 'r', 's', 'q'])
        output = []
        pause = Mock()
        game = main.main(read=read, write=output.append, pause=pause)
        self.assertEqual(game.phase, 'quit')
        self.assertIn("Oh, hello, I didn't see you there.", output[0])
        self.assertIn('your trusty journal', output)
        self.assertTrue(any("Parker's knowledge: 8/8 special: 2 book(s): 0" in line for line in output))
        pause.assert_called_once_with(2)

    def test_full_terminal_win_including_library_prompt(self):
        rolls = [0, 0, 1]
        commands = ['5', 'explore', '1', 'read']
        for knowledge in range(8, 16):
            rolls.extend([1, 1, knowledge, 0])
            commands.extend(['explore', 'argue'])
        commands.append('use special')
        rng = random.Random()
        game = Game(rng=rng)
        read = Mock(side_effect=commands)
        output = []
        with patch.object(main, 'Game', return_value=game), patch.object(rng, 'randint', side_effect=rolls):
            main.main(read=read, write=output.append, pause=lambda _: None)
        self.assertEqual(game.phase, 'won')
        self.assertIn('THE END', output)
        self.assertEqual(read.call_count, len(commands))
        self.assertEqual(read.call_args_list[2].args[0], 'Book choice =')

    def test_terminal_stops_prompting_after_defeat(self):
        rng = random.Random()
        game = Game(rng=rng)
        read = Mock(side_effect=['5', 'explore', 'read', 'read'])
        output = []
        with patch.object(main, 'Game', return_value=game), \
             patch.object(rng, 'randint', side_effect=[1, 6, 6, 0, 6, 0]):
            main.main(read=read, write=output.append, pause=lambda _: None)
        self.assertEqual(game.phase, 'lost')
        self.assertEqual(read.call_count, 4)
        self.assertTrue(any('Please reload the program' in line for line in output))
        self.assertNotIn('THE END', output)

    def test_eof_and_keyboard_interrupt_end_session_cleanly(self):
        for exception in (EOFError, KeyboardInterrupt):
            with self.subTest(exception=exception):
                game = main.main(read=Mock(side_effect=exception), write=lambda _: None, pause=lambda _: None)
                self.assertEqual(game.phase, 'quit')

    def test_running_main_twice_starts_fresh_sessions(self):
        first = main.main(read=Mock(side_effect=['5', 'read', 'quit']), write=lambda _: None, pause=lambda _: None)
        second = main.main(read=Mock(side_effect=['1', 'quit']), write=lambda _: None, pause=lambda _: None)
        self.assertEqual((first.player.name, first.player.books), ('Parker', 0))
        self.assertEqual((second.player.name, second.player.books), ('Corey', 1))
        self.assertEqual(second.player.knowledge, 7)


if __name__ == '__main__':
    unittest.main()

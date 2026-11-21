"""Check normal play and the bugs found in the original game."""

import unittest
from unittest.mock import patch

from scripts.classes import Sagan
from scripts.engine import Game


class GameTests(unittest.TestCase):
    def game(self):
        game = Game()
        game.start()
        game.submit('5')
        return game

    def boss_game(self):
        game = self.game()
        game.player.knowledge = 15
        game.player.knowledge_max = 16
        game.submit('read')
        return game

    def test_character_choice_is_validated_and_keeps_parker_special(self):
        game = Game()
        for choice in ('', 'hello', '1 + 1'):
            game.submit(choice)
            self.assertEqual(game.phase, 'character_selection')
        game.submit('5')
        self.assertEqual(game.player.name, 'Parker')
        self.assertEqual(game.player.specialname, 'REKRAP ASTRAL PLANE!')

    def test_backpack_and_reading_when_empty(self):
        game = self.game()
        self.assertEqual(game.submit('b'), ['your trusty journal'])
        game.submit('r')
        game.submit('f')  # Lose one knowledge without an enemy present.
        messages = game.submit('r')
        self.assertEqual((game.player.knowledge, game.player.books), (7, 0))
        self.assertTrue(any('backpack is empty' in line for line in messages))

    def test_library_choice_is_a_separate_turn(self):
        game = self.game()
        with patch.object(game.player.rng, 'randint', side_effect=[0, 0, 1]):
            game.submit('e')
        self.assertEqual(game.phase, 'book_selection')
        game.submit('read')  # Invalid choices leave the menu open.
        self.assertEqual(game.player.books, 1)
        game.submit('1')
        self.assertEqual(game.phase, 'exploration')
        self.assertIn(Sagan, game.player.playerbooks)

    def test_backpack_displays_and_uses_every_book(self):
        game = self.game()
        with patch.object(game.player.rng, 'randint', side_effect=[0, 0, 1] * 7):
            for _ in range(7):
                game.submit('e')
                game.submit('1')
        self.assertEqual(len(game.submit('b')), 8)
        for _ in range(8):
            game.player.knowledge = 7
            game.submit('r')
        self.assertEqual(game.player.books, 0)

    def test_special_defeats_enemy_and_charges_stop_at_zero(self):
        game = self.game()
        with patch.object(game.player.rng, 'randint', side_effect=[1, 3]):
            game.submit('e')
        enemy = game.player.enemy
        game.submit('use special')
        self.assertEqual(enemy.knowledge, 0)
        self.assertEqual((game.player.knowledge, game.player.knowledge_max), (8, 8))
        for _ in range(3):
            game.submit('u')
        self.assertEqual(game.player.special_charges, 0)
        self.assertEqual(game.player.knowledge, 7)

    def test_boss_escape_does_not_win_and_resumes_same_boss(self):
        game = self.boss_game()
        boss = game.boss
        boss.knowledge = 12
        with patch.object(game.player.rng, 'randint', side_effect=[21, 1]):
            game.submit('f')
        self.assertEqual(game.phase, 'exploration')
        self.assertFalse(game.finished)
        game.submit('e')
        self.assertIs(game.player.enemy, boss)
        self.assertEqual(boss.knowledge, 12)

    def test_boss_can_defeat_player(self):
        game = self.boss_game()
        with patch.object(game.player.rng, 'randint', side_effect=[20, 0]):
            game.submit('r')
        self.assertEqual(game.phase, 'lost')
        self.assertTrue(game.finished)

    def test_exploration_paths_keep_their_original_effects(self):
        for rolls, text, knowledge in (
            ([0, 1], 'flyer', 7),
            ([0, 0, 0, 1], 'walked in a circle', 6),
            ([0, 0, 0, 0], 'ventures further', 7),
        ):
            game = self.game()
            with patch.object(game.player.rng, 'randint', side_effect=rolls):
                messages = game.submit('e')
            self.assertIn(text, '\n'.join(messages))
            self.assertEqual(game.player.knowledge, knowledge)

    def test_complete_game_from_selection_to_victory(self):
        game = self.game()
        game.submit('r')
        for knowledge in range(8, 16):
            with patch.object(game.player.rng, 'randint', side_effect=[1, 1, knowledge, 0]):
                game.submit('e')
                game.submit('a')
        self.assertEqual(game.phase, 'boss_combat')
        self.assertIn('THE END', game.submit('u'))
        self.assertTrue(game.finished)


if __name__ == '__main__':
    unittest.main()

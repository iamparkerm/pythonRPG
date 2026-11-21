"""Regression and session tests for the shared Python game engine."""

import json
import random
import unittest
from unittest.mock import patch

from scripts.classes import BOOK_CHOICES, journal
from scripts.engine import Game


class ScriptedRandom:
    """Force branches while checking that rolls remain within the game's bounds."""

    def __init__(self, integers=(), selections=()):
        self.integers = iter(integers)
        self.selections = iter(selections)

    def randint(self, low, high):
        value = next(self.integers)
        if not low <= value <= high:
            raise AssertionError('Scripted roll {} outside {}..{}'.format(value, low, high))
        return value

    def choice(self, sequence):
        return sequence[next(self.selections, 0)]


class EngineTests(unittest.TestCase):
    def game(self, integers=(), selections=()):
        game = Game(rng=ScriptedRandom(integers, selections))
        game.start()
        game.submit('5')
        return game

    def boss_game(self, integers=()):
        game = self.game(integers)
        game.player.knowledge = 15
        game.player.knowledge_max = 16
        result = game.submit('read')
        self.assertEqual(result['phase'], 'boss_combat')
        return game

    def test_start_is_idempotent_and_returns_five_characters(self):
        game = Game()
        result = game.start()
        self.assertEqual(result['phase'], 'character_selection')
        self.assertEqual(len(result['choices']), 5)
        self.assertEqual(game.start()['messages'], [])

    def test_all_characters_and_original_parker_special(self):
        for choice, name in enumerate(('Corey', 'Eric', 'Josh', 'Kevin', 'Parker'), 1):
            with self.subTest(choice=choice):
                game = Game()
                game.start()
                result = game.submit(str(choice))
                self.assertEqual(result['state']['player']['name'], name)
                self.assertEqual(result['phase'], 'exploration')
        self.assertEqual(game.player.specialname, 'REKRAP ASTRAL PLANE!')

    def test_invalid_character_choices_never_execute_expressions(self):
        game = Game()
        game.start()
        for choice in ('', 'hello', '0', '6', '1.0', 'True', '1 + 1', '__import__("os").getcwd()'):
            with self.subTest(choice=choice), patch('builtins.eval', side_effect=AssertionError('eval called')):
                result = game.submit(choice)
                self.assertEqual(result['phase'], 'character_selection')
                self.assertEqual(game.player.name, '')
                self.assertTrue(result['messages'])

    def test_requires_start_before_actions(self):
        with self.assertRaises(RuntimeError):
            Game().submit('1')

    def test_initial_backpack_shows_journal_without_empty_message(self):
        result = self.game().submit('backpack')
        self.assertEqual(result['messages'], ['your trusty journal'])

    def test_empty_read_neither_crashes_nor_awards_knowledge(self):
        game = self.game()
        game.submit('read')
        game.submit('flee')  # Original penalty: 8 -> 7 when no enemy is present.
        result = game.submit('read')
        self.assertEqual(game.player.knowledge, 7)
        self.assertEqual(game.player.books, 0)
        self.assertTrue(any('backpack is empty' in message for message in result['messages']))

    def test_library_waits_for_a_separate_validated_choice(self):
        game = self.game([0, 0, 1])
        result = game.submit('explore')
        self.assertEqual(result['phase'], 'book_selection')
        self.assertEqual(len(result['choices']), 6)
        self.assertEqual(game.player.books, 1)
        for choice in ('', 'read', '9', '1 + 1'):
            self.assertEqual(game.submit(choice)['phase'], 'book_selection')
            self.assertEqual(game.player.books, 1)
        self.assertEqual(game.submit('1')['phase'], 'exploration')
        self.assertEqual(game.player.books, 2)
        self.assertIn(BOOK_CHOICES['1'], game.player.playerbooks)

    def test_all_library_books_can_be_selected(self):
        for choice, book in BOOK_CHOICES.items():
            with self.subTest(choice=choice):
                game = self.game([0, 0, 1])
                game.submit('explore')
                game.submit(choice)
                self.assertIn(book, game.player.playerbooks)

    def test_library_can_be_skipped(self):
        game = self.game([0, 0, 1])
        game.submit('explore')
        self.assertEqual(game.submit('0')['phase'], 'exploration')
        self.assertEqual(game.player.books, 1)

    def test_backpack_displays_more_than_six_books_and_count_stays_correct(self):
        game = self.game([0, 0, 1] * 7)
        for _ in range(7):
            game.submit('explore')
            game.submit('1')
        result = game.submit('backpack')
        self.assertEqual(game.player.books, 8)
        self.assertEqual(len(result['messages']), 8)
        for _ in range(8):
            game.player.knowledge = 7
            game.submit('read')
        self.assertEqual(game.player.books, 0)

    def test_reading_preserves_original_author_priority(self):
        game = self.game()
        game.player.playerbooks = [journal, BOOK_CHOICES['5'], BOOK_CHOICES['2'], BOOK_CHOICES['1']]
        result = game.submit('read')
        self.assertIn(BOOK_CHOICES['1'][1], result['messages'][1])
        self.assertNotIn(BOOK_CHOICES['1'], game.player.playerbooks)

    def test_each_exploration_branch(self):
        branches = (
            ([0, 1], 'flyer', 7),
            ([0, 0, 0, 1], 'walked in a circle', 6),
            ([0, 0, 0, 0], 'ventures further', 7),
        )
        for rolls, message, knowledge in branches:
            with self.subTest(message=message):
                game = self.game(rolls)
                result = game.submit('explore')
                self.assertTrue(any(message in line for line in result['messages']))
                self.assertEqual(game.player.knowledge, knowledge)

    def test_enemy_generation_uses_the_injected_rng_for_stats_name_and_quote(self):
        game = self.game([1, 3], [2, 4])
        result = game.submit('explore')
        self.assertEqual(result['phase'], 'combat')
        self.assertEqual(result['state']['enemy'], {'name': 'White Knight', 'knowledge': 3})
        self.assertIn('patriarchy', result['messages'][-1])

    def test_enemy_generation_at_one_knowledge_is_valid(self):
        game = self.game([1])
        game.player.knowledge = 1
        game.submit('explore')
        self.assertEqual(game.player.enemy.knowledge, 1)

    def test_failed_attack_allows_retaliation_and_successful_attack_does_not(self):
        game = self.game([1, 1, 0, 1, 1, 0, 6, 0])
        game.submit('explore')
        self.assertEqual(game.submit('argue')['phase'], 'combat')
        self.assertEqual(game.player.knowledge, 6)
        self.assertEqual(game.submit('argue')['phase'], 'exploration')
        self.assertEqual((game.player.knowledge, game.player.knowledge_max), (7, 9))

    def test_special_reduces_enemy_to_zero_and_preserves_original_reward(self):
        game = self.game([1, 3])
        game.submit('explore')
        enemy = game.player.enemy
        result = game.submit('use special')
        self.assertEqual(enemy.knowledge, 0)
        self.assertEqual(result['phase'], 'exploration')
        self.assertEqual((game.player.knowledge, game.player.knowledge_max), (8, 8))
        self.assertEqual(game.player.special_charges, 1)

    def test_special_charges_stop_at_zero_outside_combat(self):
        game = self.game()
        for _ in range(4):
            game.submit('u')
        self.assertEqual(game.player.special_charges, 0)
        self.assertEqual(game.player.knowledge, 5)

    def test_exhausted_special_in_combat_allows_retaliation(self):
        game = self.game([1, 1, 1, 0])
        game.submit('explore')
        game.player.special_charges = 0
        self.assertEqual(game.submit('u')['phase'], 'combat')
        self.assertEqual(game.player.knowledge, 6)

    def test_read_and_explore_in_combat_allow_retaliation(self):
        for command in ('read', 'explore'):
            with self.subTest(command=command):
                game = self.game([1, 1, 1, 0])
                game.submit('explore')
                self.assertEqual(game.submit(command)['phase'], 'combat')
                self.assertEqual(game.player.knowledge, 6)
                self.assertEqual(game.player.books, 1)

    def test_failed_flee_allows_retaliation(self):
        game = self.game([1, 3, 1, 3, 3, 0])
        game.submit('explore')
        self.assertEqual(game.submit('flee')['phase'], 'combat')
        self.assertEqual(game.player.knowledge, 4)

    def test_boss_flee_does_not_win_and_next_explore_resumes_same_boss(self):
        game = self.boss_game([21, 1])
        boss = game.boss
        boss.knowledge = 12
        result = game.submit('flee')
        self.assertEqual(result['phase'], 'exploration')
        self.assertFalse(result['finished'])
        self.assertFalse(any('THE END' in line for line in result['messages']))
        self.assertEqual(game.submit('explore')['phase'], 'boss_combat')
        self.assertIs(game.player.enemy, boss)
        self.assertEqual(boss.knowledge, 12)

    def test_boss_death_ends_game_immediately(self):
        game = self.boss_game([20, 0])
        result = game.submit('read')
        self.assertEqual(game.player.knowledge, 0)
        self.assertEqual(result['phase'], 'lost')
        self.assertTrue(result['finished'])
        self.assertIsNone(result['prompt'])
        self.assertEqual(game.submit('use special')['phase'], 'lost')
        self.assertEqual(game.boss.knowledge, 20)

    def test_normal_combat_death_ends_game(self):
        game = self.game([1, 6, 6, 0, 6, 0])
        game.submit('explore')
        self.assertEqual(game.submit('read')['phase'], 'combat')
        result = game.submit('read')
        self.assertEqual(result['phase'], 'lost')
        self.assertEqual(game.player.knowledge, 0)
        self.assertIsNone(game.boss)

    def test_normal_boss_kill_wins(self):
        game = self.boss_game([16, 0])
        game.boss.knowledge = 1
        result = game.submit('argue')
        self.assertEqual(result['phase'], 'won')
        self.assertIn('THE END', result['messages'])
        self.assertTrue(result['finished'])
        self.assertEqual(result['choices'], [])

    def test_special_boss_kill_wins(self):
        game = self.boss_game()
        self.assertEqual(game.submit('u')['phase'], 'won')
        self.assertEqual(game.boss.knowledge, 0)
        self.assertEqual(game.submit('e')['messages'], [])

    def test_boss_starts_when_victory_reaches_sixteen(self):
        game = self.game([1, 1, 15, 0])
        game.player.knowledge = 15
        game.player.knowledge_max = 16
        game.submit('explore')
        self.assertEqual(game.submit('argue')['phase'], 'boss_combat')
        self.assertEqual(game.player.knowledge, 16)

    def test_first_letter_commands_and_normalized_full_command(self):
        for command in ('h', 's', 'b', 'a', 'r', 'f', 'u', ' USE   SPECIAL '):
            with self.subTest(command=command):
                result = self.game().submit(command)
                self.assertFalse(any("doesn't understand" in message for message in result['messages']))

    def test_unknown_commands_are_safe_and_do_not_ignore_extra_words(self):
        game = self.game()
        for command in ('xyz', 'use nonsense', 'argue extra'):
            result = game.submit(command)
            self.assertEqual(result['phase'], 'exploration')
            self.assertIn("doesn't understand", result['messages'][0])
        self.assertEqual(game.player.knowledge, 7)
        self.assertEqual(game.submit('   ')['messages'], [])

    def test_quit_works_in_each_interactive_phase(self):
        selection = Game()
        selection.start()
        exploration = self.game()
        library = self.game([0, 0, 1])
        library.submit('e')
        combat = self.game([1, 1])
        combat.submit('e')
        for game in (selection, exploration, library, combat, self.boss_game()):
            with self.subTest(phase=game.phase):
                self.assertEqual(game.submit('q')['phase'], 'quit')
                before = game.player.knowledge
                self.assertEqual(game.submit('r')['messages'], [])
                self.assertEqual(game.player.knowledge, before)

    def test_all_quit_prefixes_finish_the_session(self):
        for command in ('q', 'qu', 'qui', 'quit'):
            with self.subTest(command=command):
                self.assertTrue(self.game().submit(command)['finished'])

    def test_sessions_and_returned_snapshots_are_independent(self):
        first = self.game()
        second = self.game()
        snapshot = first.submit('stats')
        snapshot['state']['player']['books'][0]['title'] = 'Changed'
        snapshot['messages'].append('Changed')
        first.submit('read')
        self.assertEqual(second.player.books, 1)
        self.assertEqual(second.player.playerbooks[0][1], 'your trusty journal')
        self.assertEqual(second.player.knowledge, 7)
        self.assertNotIn('Changed', first.submit('s')['messages'])

    def test_seeded_games_replay_identically(self):
        first = Game(rng=random.Random(123))
        second = Game(rng=random.Random(123))
        self.assertEqual(first.start(), second.start())
        for command in ('5', 'read', 'explore', '1', 'argue', 'use special', 'flee', 'stats', 'quit'):
            self.assertEqual(first.submit(command), second.submit(command))

    def test_engine_never_uses_terminal_io_sleep_eval_or_process_exit(self):
        with patch('builtins.input', side_effect=AssertionError('input called')), \
             patch('builtins.print', side_effect=AssertionError('print called')), \
             patch('builtins.eval', side_effect=AssertionError('eval called')), \
             patch('sys.exit', side_effect=AssertionError('exit called')), \
             patch('builtins.exit', side_effect=AssertionError('exit called')), \
             patch('time.sleep', side_effect=AssertionError('sleep called')):
            game = self.game([0, 0, 1])
            for command in ('explore', '1', 'read', 'quit'):
                json.dumps(game.submit(command))
            boss_game = self.boss_game()
            json.dumps(boss_game.submit('u'))

    def test_complete_playthrough_from_selection_to_boss_victory(self):
        rolls = [0, 0, 1]
        for knowledge in range(8, 16):
            rolls.extend([1, 1, knowledge, 0])
        game = self.game(rolls)
        self.assertEqual(game.submit('explore')['phase'], 'book_selection')
        game.submit('1')
        game.submit('read')
        for _ in range(8):
            self.assertEqual(game.submit('explore')['phase'], 'combat')
            game.submit('argue')
        self.assertEqual(game.phase, 'boss_combat')
        self.assertEqual(game.player.knowledge, 16)
        result = game.submit('use special')
        self.assertEqual(result['phase'], 'won')
        self.assertIn('THE END', result['messages'])
        json.dumps(result)


if __name__ == '__main__':
    unittest.main()

"""Protect working rules from the original terminal game before extraction."""

import unittest
from unittest.mock import patch

from scripts import classes


class OriginalRulesTests(unittest.TestCase):
    def test_starting_player(self):
        player = classes.Player()
        self.assertEqual((player.knowledge, player.knowledge_max), (7, 8))
        self.assertEqual(player.books, 1)
        self.assertIn(classes.journal, player.playerbooks)

    def test_read_journal_consumes_it_and_restores_one_knowledge(self):
        player = classes.Player()
        player.name = "Parker"
        player.read()
        output = '\n'.join(player.messages)
        self.assertEqual((player.knowledge, player.books), (8, 0))
        self.assertIn("Remember to check off your habitica dailies.", output)
        self.assertIn("Parker feels smarter!", output)

    def test_read_at_maximum_preserves_books(self):
        player = classes.Player()
        player.knowledge = player.knowledge_max
        player.read()
        self.assertEqual(player.books, 1)

    def test_ordinary_victory_rewards_current_and_maximum_knowledge(self):
        player = classes.Player()
        enemy = classes.Character()
        enemy.name = "Opponent"
        player.enemy = enemy
        player.state = "argue"
        with patch.object(player.rng, "randint", side_effect=[7, 0]):
            player.argue()
        self.assertEqual(enemy.knowledge, 0)
        self.assertEqual((player.knowledge, player.knowledge_max), (8, 9))
        self.assertEqual(player.state, "normal")
        self.assertIsNone(player.enemy)
        self.assertIn("vanquishes the Opponent!", '\n'.join(player.messages))

    def test_zero_damage_counters_without_healing(self):
        player = classes.Player()
        enemy = classes.Character()
        with patch.object(player.rng, "randint", side_effect=[0, 1]):
            player.do_damage(enemy)
        self.assertEqual(enemy.knowledge, 1)

    def test_wandering_penalty_stops_at_one(self):
        player = classes.Player()
        player.knowledge = 1
        player.dumber()
        self.assertEqual(player.knowledge, 1)

    def test_boss_starts_at_twenty(self):
        self.assertEqual(classes.Boss().knowledge, 20)


if __name__ == "__main__":
    unittest.main()

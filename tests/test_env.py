import random
import unittest

from src.game.env import Game2048Env


class TestGame2048Env(unittest.TestCase):
    def test_reset_creates_valid_start(self):
        env = Game2048Env(rng=random.Random(42))
        board = env.reset()

        non_zero = [cell for row in board for cell in row if cell != 0]
        self.assertEqual(len(non_zero), 2)
        for value in non_zero:
            self.assertIn(value, [2, 4])

    def test_getters_work(self):
        env = Game2048Env(rng=random.Random(42))
        self.assertEqual(env.get_score(), 0)
        self.assertEqual(env.get_move_count(), 0)
        self.assertGreaterEqual(env.get_max_tile(), 2)

    def test_step_returns_expected_structure(self):
        env = Game2048Env(rng=random.Random(42))
        legal = env.get_legal_moves()
        action = legal[0]

        board, reward, done, info = env.step(action)

        self.assertIsInstance(board, list)
        self.assertIsInstance(reward, int)
        self.assertIsInstance(done, bool)
        self.assertIsInstance(info, dict)

        self.assertIn("changed", info)
        self.assertIn("score", info)
        self.assertIn("max_tile", info)
        self.assertIn("won", info)
        self.assertIn("move_count", info)
        self.assertIn("legal_moves", info)

    def test_step_updates_move_count_when_changed(self):
        env = Game2048Env(rng=random.Random(42))
        legal = env.get_legal_moves()
        action = legal[0]

        _, _, _, info = env.step(action)
        self.assertEqual(info["move_count"], 1)

    def test_step_after_done_raises(self):
        env = Game2048Env(rng=random.Random(42))
        env.done = True

        with self.assertRaises(RuntimeError):
            env.step("left")


if __name__ == "__main__":
    unittest.main()
import unittest

from src.game.state import get_max_tile, get_score_after_move, has_won, is_game_over


class TestState(unittest.TestCase):
    def test_get_score_after_move(self):
        self.assertEqual(get_score_after_move(0, 4), 4)
        self.assertEqual(get_score_after_move(20, 16), 36)

    def test_get_max_tile(self):
        board = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [2, 4, 8, 16],
            [32, 64, 128, 1024],
        ]
        self.assertEqual(get_max_tile(board), 1024)

    def test_has_won_false(self):
        board = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [2, 4, 8, 16],
            [32, 64, 128, 1024],
        ]
        self.assertFalse(has_won(board))

    def test_has_won_true(self):
        board = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [2, 4, 8, 16],
            [32, 64, 128, 2048],
        ]
        self.assertTrue(has_won(board))

    def test_is_game_over_true(self):
        board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ]
        self.assertTrue(is_game_over(board))

    def test_is_game_over_false(self):
        board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 0],
        ]
        self.assertFalse(is_game_over(board))


if __name__ == "__main__":
    unittest.main()
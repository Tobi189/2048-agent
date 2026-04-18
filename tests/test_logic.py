import unittest

from src.game.logic import (
    apply_move,
    compress_line_left,
    get_legal_moves,
    has_legal_moves,
    merge_line_left,
    move_down,
    move_left,
    move_right,
    move_up,
    process_line_left,
)


class TestLogic(unittest.TestCase):
    def test_compress_line_left(self):
        self.assertEqual(compress_line_left([2, 0, 2, 4]), [2, 2, 4, 0])
        self.assertEqual(compress_line_left([0, 0, 2, 0]), [2, 0, 0, 0])
        self.assertEqual(compress_line_left([0, 0, 0, 0]), [0, 0, 0, 0])

    def test_merge_line_left_simple(self):
        merged, reward = merge_line_left([2, 2, 4, 0])
        self.assertEqual(merged, [4, 4, 0, 0])
        self.assertEqual(reward, 4)

    def test_merge_line_left_double_pair(self):
        merged, reward = merge_line_left([2, 2, 2, 2])
        self.assertEqual(merged, [4, 4, 0, 0])
        self.assertEqual(reward, 8)

    def test_merge_line_left_no_double_merge(self):
        merged, reward = process_line_left([2, 2, 4, 4])
        self.assertEqual(merged, [4, 8, 0, 0])
        self.assertEqual(reward, 12)

    def test_process_line_left(self):
        merged, reward = process_line_left([2, 0, 2, 4])
        self.assertEqual(merged, [4, 4, 0, 0])
        self.assertEqual(reward, 4)

    def test_move_left(self):
        board = [
            [2, 0, 2, 4],
            [0, 4, 4, 0],
            [2, 2, 2, 0],
            [0, 0, 0, 2],
        ]
        expected = [
            [4, 4, 0, 0],
            [8, 0, 0, 0],
            [4, 2, 0, 0],
            [2, 0, 0, 0],
        ]
        new_board, reward, changed = move_left(board)
        self.assertEqual(new_board, expected)
        self.assertEqual(reward, 16)
        self.assertTrue(changed)

    def test_move_right(self):
        board = [
            [2, 0, 2, 4],
            [0, 4, 4, 0],
            [2, 2, 2, 0],
            [0, 0, 0, 2],
        ]
        expected = [
            [0, 0, 4, 4],
            [0, 0, 0, 8],
            [0, 0, 2, 4],
            [0, 0, 0, 2],
        ]
        new_board, reward, changed = move_right(board)
        self.assertEqual(new_board, expected)
        self.assertEqual(reward, 16)
        self.assertTrue(changed)

    def test_move_up(self):
        board = [
            [2, 0, 2, 4],
            [2, 4, 0, 4],
            [0, 4, 2, 0],
            [0, 0, 2, 0],
        ]
        expected = [
            [4, 8, 4, 8],
            [0, 0, 2, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        new_board, reward, changed = move_up(board)
        self.assertEqual(new_board, expected)
        self.assertEqual(reward, 24)
        self.assertTrue(changed)

    def test_move_down(self):
        board = [
            [2, 0, 2, 4],
            [2, 4, 0, 4],
            [0, 4, 2, 0],
            [0, 0, 2, 0],
        ]
        expected = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 2, 0],
            [4, 8, 4, 8],
        ]
        new_board, reward, changed = move_down(board)
        self.assertEqual(new_board, expected)
        self.assertEqual(reward, 24)
        self.assertTrue(changed)

    def test_apply_move_invalid(self):
        board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        with self.assertRaises(ValueError):
            apply_move(board, "diagonal")

    def test_has_legal_moves_true(self):
        board = [
            [2, 0, 4, 8],
            [16, 32, 64, 128],
            [2, 4, 8, 16],
            [32, 64, 128, 256],
        ]
        self.assertTrue(has_legal_moves(board))

    def test_has_legal_moves_false(self):
        board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ]
        self.assertFalse(has_legal_moves(board))

    def test_get_legal_moves(self):
        board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 0],
        ]
        legal = get_legal_moves(board)
        self.assertNotIn("left", legal)
        self.assertIn("right", legal)
        self.assertIn("down", legal)
        self.assertNotIn("up", legal)


if __name__ == "__main__":
    unittest.main()
import random
import unittest

from src.game.board import bitboard_to_board, board_to_bitboard, get_empty_cells
from src.game.spawn import (
    choose_new_tile_value,
    create_initial_bitboard,
    create_initial_board,
    spawn_random_tile,
    spawn_random_tile_bitboard,
)


class TestSpawn(unittest.TestCase):
    def test_choose_new_tile_value(self):
        rng = random.Random(42)
        values = [choose_new_tile_value(rng) for _ in range(100)]

        for value in values:
            self.assertIn(value, [2, 4])

    def test_spawn_random_tile_on_empty_board(self):
        board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        rng = random.Random(42)

        new_board = spawn_random_tile(board, rng)

        non_zero_values = [cell for row in new_board for cell in row if cell != 0]
        self.assertEqual(len(non_zero_values), 1)
        self.assertIn(non_zero_values[0], [2, 4])

    def test_spawn_random_tile_does_not_modify_original(self):
        board = [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        original_copy = [row[:] for row in board]
        rng = random.Random(42)

        _ = spawn_random_tile(board, rng)

        self.assertEqual(board, original_copy)

    def test_spawn_random_tile_when_board_full(self):
        board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ]
        rng = random.Random(42)

        new_board = spawn_random_tile(board, rng)
        self.assertEqual(new_board, board)

    def test_create_initial_board(self):
        rng = random.Random(42)
        board = create_initial_board(rng)

        non_zero_values = [cell for row in board for cell in row if cell != 0]
        self.assertEqual(len(non_zero_values), 2)

        for value in non_zero_values:
            self.assertIn(value, [2, 4])

    def test_create_initial_board_has_14_empty_cells(self):
        rng = random.Random(42)
        board = create_initial_board(rng)

        empty_cells = get_empty_cells(board)
        self.assertEqual(len(empty_cells), 14)

    def test_spawn_random_tile_bitboard(self):
        board = [
            [0, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        bitboard = board_to_bitboard(board)
        rng = random.Random(42)

        new_bitboard = spawn_random_tile_bitboard(bitboard, rng)
        new_board = bitboard_to_board(new_bitboard)

        non_zero_values = [cell for row in new_board for cell in row if cell != 0]
        self.assertEqual(len(non_zero_values), 2)
        self.assertIn(2, non_zero_values)

    def test_create_initial_bitboard(self):
        rng = random.Random(42)
        bitboard = create_initial_bitboard(rng)
        board = bitboard_to_board(bitboard)

        non_zero_values = [cell for row in board for cell in row if cell != 0]
        self.assertEqual(len(non_zero_values), 2)
        for value in non_zero_values:
            self.assertIn(value, [2, 4])


if __name__ == "__main__":
    unittest.main()
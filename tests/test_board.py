import unittest

from src.game.board import (
    bitboard_to_board,
    board_to_bitboard,
    create_empty_board,
    exponent_to_tile,
    get_cell_exponent,
    get_empty_cells,
    set_cell_exponent,
    tile_to_exponent,
)


class TestBoardBitboard(unittest.TestCase):
    def test_create_empty_board(self):
        board = create_empty_board()
        self.assertEqual(board, [[0, 0, 0, 0] for _ in range(4)])

    def test_tile_exponent_roundtrip(self):
        values = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
        for value in values:
            exp = tile_to_exponent(value)
            self.assertEqual(exponent_to_tile(exp), value)

    def test_board_bitboard_roundtrip(self):
        board = [
            [2, 0, 4, 8],
            [16, 32, 64, 128],
            [256, 512, 1024, 0],
            [0, 2, 4, 8],
        ]
        bitboard = board_to_bitboard(board)
        restored = bitboard_to_board(bitboard)
        self.assertEqual(restored, board)

    def test_get_and_set_cell_exponent(self):
        bitboard = 0
        bitboard = set_cell_exponent(bitboard, 0, 1)   # 2
        bitboard = set_cell_exponent(bitboard, 5, 3)   # 8
        bitboard = set_cell_exponent(bitboard, 15, 11) # 2048

        self.assertEqual(get_cell_exponent(bitboard, 0), 1)
        self.assertEqual(get_cell_exponent(bitboard, 5), 3)
        self.assertEqual(get_cell_exponent(bitboard, 15), 11)

        board = bitboard_to_board(bitboard)
        self.assertEqual(board[0][0], 2)
        self.assertEqual(board[1][1], 8)
        self.assertEqual(board[3][3], 2048)

    def test_get_empty_cells(self):
        board = [
            [2, 0, 4, 0],
            [0, 32, 64, 128],
            [256, 0, 1024, 0],
            [0, 2, 4, 8],
        ]
        empties = get_empty_cells(board)
        self.assertEqual(
            sorted(empties),
            sorted([(0, 1), (0, 3), (1, 0), (2, 1), (2, 3), (3, 0)]),
        )


if __name__ == "__main__":
    unittest.main()
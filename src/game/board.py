from __future__ import annotations

from typing import List, Tuple

Board = List[List[int]]
BitBoard = int
Position = Tuple[int, int]

BOARD_SIZE = 4
CELL_COUNT = BOARD_SIZE * BOARD_SIZE
NIBBLE_MASK = 0xF
MAX_BITBOARD = (1 << 64) - 1


def create_empty_board(size: int = BOARD_SIZE) -> Board:
    if size <= 0:
        raise ValueError("Board size must be a positive integer.")
    return [[0 for _ in range(size)] for _ in range(size)]


def validate_board(board: Board) -> None:
    if not isinstance(board, list) or not board:
        raise ValueError("Board must be a non-empty 2D list.")

    if not all(isinstance(row, list) for row in board):
        raise ValueError("Board must be a 2D list.")

    size = len(board)

    for row in board:
        if len(row) != size:
            raise ValueError("Board must be square.")
        for value in row:
            if not isinstance(value, int):
                raise TypeError("All board values must be integers.")
            if value < 0:
                raise ValueError("Board values cannot be negative.")


def validate_bitboard(bitboard: BitBoard) -> None:
    if not isinstance(bitboard, int):
        raise TypeError("BitBoard must be an integer.")
    if bitboard < 0:
        raise ValueError("BitBoard cannot be negative.")
    if bitboard > MAX_BITBOARD:
        raise ValueError("BitBoard must fit into 64 bits.")


def copy_board(board: Board) -> Board:
    validate_board(board)
    return [row[:] for row in board]


def get_empty_cells(board: Board) -> List[Position]:
    validate_board(board)

    empty_cells: List[Position] = []
    for row_idx, row in enumerate(board):
        for col_idx, value in enumerate(row):
            if value == 0:
                empty_cells.append((row_idx, col_idx))

    return empty_cells


def get_board_size(board: Board) -> int:
    validate_board(board)
    return len(board)


def print_board(board: Board) -> None:
    validate_board(board)

    cell_width = max(
        4,
        max(len(str(value)) for row in board for value in row if value != 0)
        if any(value != 0 for row in board for value in row)
        else 4,
    )

    horizontal = "+" + "+".join(["-" * cell_width for _ in range(len(board))]) + "+"

    print(horizontal)
    for row in board:
        formatted_row = []
        for value in row:
            display = "." if value == 0 else str(value)
            formatted_row.append(display.rjust(cell_width))
        print("|" + "|".join(formatted_row) + "|")
        print(horizontal)


def tile_to_exponent(value: int) -> int:
    if not isinstance(value, int):
        raise TypeError("Tile values must be integers.")
    if value < 0:
        raise ValueError("Tile values cannot be negative.")
    if value == 0:
        return 0
    if value & (value - 1):
        raise ValueError("Non-zero tile values must be powers of two.")
    return value.bit_length() - 1


def exponent_to_tile(exp: int) -> int:
    if not isinstance(exp, int):
        raise TypeError("Exponent must be an integer.")
    if exp < 0:
        raise ValueError("Exponent cannot be negative.")
    return 0 if exp == 0 else (1 << exp)


def get_cell_exponent(bitboard: BitBoard, idx: int) -> int:
    validate_bitboard(bitboard)
    if not 0 <= idx < CELL_COUNT:
        raise IndexError("Cell index out of range.")
    return (bitboard >> (4 * idx)) & NIBBLE_MASK


def set_cell_exponent(bitboard: BitBoard, idx: int, exp: int) -> BitBoard:
    validate_bitboard(bitboard)
    if not 0 <= idx < CELL_COUNT:
        raise IndexError("Cell index out of range.")
    if not isinstance(exp, int):
        raise TypeError("Exponent must be an integer.")
    if not 0 <= exp <= NIBBLE_MASK:
        raise ValueError("Exponent must fit in 4 bits (0..15).")

    shift = 4 * idx
    cleared = bitboard & ~(NIBBLE_MASK << shift)
    return cleared | (exp << shift)


def board_to_bitboard(board: Board) -> BitBoard:
    validate_board(board)

    if len(board) != BOARD_SIZE:
        raise ValueError("Only 4x4 boards are supported by the bitboard backend.")

    bitboard = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            idx = r * BOARD_SIZE + c
            exp = tile_to_exponent(board[r][c])
            bitboard |= exp << (4 * idx)

    return bitboard


def bitboard_to_board(bitboard: BitBoard) -> Board:
    validate_bitboard(bitboard)

    board = create_empty_board(BOARD_SIZE)
    for idx in range(CELL_COUNT):
        r = idx // BOARD_SIZE
        c = idx % BOARD_SIZE
        exp = (bitboard >> (4 * idx)) & NIBBLE_MASK
        board[r][c] = exponent_to_tile(exp)

    return board


def get_empty_positions_bitboard(bitboard: BitBoard) -> List[int]:
    validate_bitboard(bitboard)
    return [idx for idx in range(CELL_COUNT) if ((bitboard >> (4 * idx)) & NIBBLE_MASK) == 0]
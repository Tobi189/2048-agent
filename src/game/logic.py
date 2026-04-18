from __future__ import annotations

from typing import List, Tuple

from .board import Board, validate_board
from .utils import reverse_rows, transpose_board

MoveResult = Tuple[Board, int, bool]
VALID_MOVES = {"left", "right", "up", "down"}


def compress_line_left(line: List[int]) -> List[int]:
    """
    Shift all non-zero values to the left, preserving order.

    Example:
        [2, 0, 2, 4] -> [2, 2, 4, 0]
    """
    non_zero = [value for value in line if value != 0]
    zeros = [0] * (len(line) - len(non_zero))
    return non_zero + zeros


def merge_line_left(line: List[int]) -> Tuple[List[int], int]:
    """
    Merge equal adjacent tiles from left to right, once per pair.

    Assumes the line is already compressed left.

    Example:
        [2, 2, 4, 0] -> ([4, 4, 0, 0], 4)
        [2, 2, 2, 2] -> ([4, 4, 0, 0], 8)
    """
    merged = line[:]
    reward = 0

    for i in range(len(merged) - 1):
        if merged[i] != 0 and merged[i] == merged[i + 1]:
            merged[i] *= 2
            reward += merged[i]
            merged[i + 1] = 0

    merged = compress_line_left(merged)
    return merged, reward


def process_line_left(line: List[int]) -> Tuple[List[int], int]:
    """
    Full left-move processing for a single row/column:
    compress -> merge -> compress
    """
    compressed = compress_line_left(line)
    merged, reward = merge_line_left(compressed)
    return merged, reward


def move_left(board: Board) -> MoveResult:
    """
    Apply a left move to the board.

    Returns:
        new_board, reward_gained, changed
    """
    validate_board(board)

    new_board: Board = []
    total_reward = 0

    for row in board:
        new_row, reward = process_line_left(row)
        new_board.append(new_row)
        total_reward += reward

    changed = new_board != board
    return new_board, total_reward, changed


def move_right(board: Board) -> MoveResult:
    """
    Apply a right move by reversing rows, moving left, then reversing back.
    """
    validate_board(board)

    reversed_board = reverse_rows(board)
    moved_board, reward, changed = move_left(reversed_board)
    restored_board = reverse_rows(moved_board)

    changed = restored_board != board
    return restored_board, reward, changed


def move_up(board: Board) -> MoveResult:
    """
    Apply an up move by transposing, moving left, then transposing back.
    """
    validate_board(board)

    transposed = transpose_board(board)
    moved_board, reward, changed = move_left(transposed)
    restored_board = transpose_board(moved_board)

    changed = restored_board != board
    return restored_board, reward, changed


def move_down(board: Board) -> MoveResult:
    """
    Apply a down move by transposing, moving right, then transposing back.
    """
    validate_board(board)

    transposed = transpose_board(board)
    moved_board, reward, changed = move_right(transposed)
    restored_board = transpose_board(moved_board)

    changed = restored_board != board
    return restored_board, reward, changed


def apply_move(board: Board, direction: str) -> MoveResult:
    """
    Apply a move in one of: left, right, up, down.
    """
    validate_board(board)

    direction = direction.lower().strip()
    if direction not in VALID_MOVES:
        raise ValueError(f"Invalid move '{direction}'. Valid moves: {sorted(VALID_MOVES)}")

    if direction == "left":
        return move_left(board)
    if direction == "right":
        return move_right(board)
    if direction == "up":
        return move_up(board)
    return move_down(board)


def has_legal_moves(board: Board) -> bool:
    """
    Return True if at least one move changes the board.
    """
    validate_board(board)

    for direction in VALID_MOVES:
        _, _, changed = apply_move(board, direction)
        if changed:
            return True
    return False


def get_legal_moves(board: Board) -> List[str]:
    """
    Return a list of moves that would change the board.
    """
    validate_board(board)

    legal_moves: List[str] = []
    for direction in ("left", "right", "up", "down"):
        _, _, changed = apply_move(board, direction)
        if changed:
            legal_moves.append(direction)

    return legal_moves
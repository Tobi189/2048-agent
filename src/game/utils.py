from __future__ import annotations

from .board import Board, validate_board


def transpose_board(board: Board) -> Board:
    validate_board(board)
    return [list(row) for row in zip(*board)]


def reverse_rows(board: Board) -> Board:
    validate_board(board)
    return [list(reversed(row)) for row in board]
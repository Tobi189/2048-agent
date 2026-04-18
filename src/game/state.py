from __future__ import annotations

from .board import Board, validate_board
from .logic import has_legal_moves


def get_score_after_move(current_score: int, move_reward: int) -> int:
    """
    Return updated score after adding reward from a move.
    """
    if current_score < 0:
        raise ValueError("Current score cannot be negative.")
    if move_reward < 0:
        raise ValueError("Move reward cannot be negative.")

    return current_score + move_reward


def get_max_tile(board: Board) -> int:
    """
    Return the largest tile currently on the board.
    """
    validate_board(board)
    return max(max(row) for row in board)


def has_won(board: Board, target: int = 2048) -> bool:
    """
    Return True if the board contains the target tile.
    """
    validate_board(board)
    return get_max_tile(board) >= target


def is_game_over(board: Board) -> bool:
    """
    Return True if no legal moves remain.
    """
    validate_board(board)
    return not has_legal_moves(board)
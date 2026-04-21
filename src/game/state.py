from __future__ import annotations

from typing import Union

from .board import Board, BitBoard, board_to_bitboard, validate_board, validate_bitboard
from .logic import has_legal_moves


def get_score_after_move(current_score: int, move_reward: int) -> int:
    if current_score < 0:
        raise ValueError("Current score cannot be negative.")
    if move_reward < 0:
        raise ValueError("Move reward cannot be negative.")

    return current_score + move_reward


def get_max_tile(board: Union[Board, BitBoard]) -> int:
    if isinstance(board, int):
        validate_bitboard(board)
        max_exp = 0
        for idx in range(16):
            exp = (board >> (4 * idx)) & 0xF
            if exp > max_exp:
                max_exp = exp
        return 0 if max_exp == 0 else (1 << max_exp)

    validate_board(board)
    return get_max_tile(board_to_bitboard(board))


def has_won(board: Union[Board, BitBoard], target: int = 2048) -> bool:
    return get_max_tile(board) >= target


def is_game_over(board: Union[Board, BitBoard]) -> bool:
    return not has_legal_moves(board)
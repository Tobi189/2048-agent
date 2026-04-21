from __future__ import annotations

import random
from typing import Optional, Union

from .board import (
    Board,
    BitBoard,
    bitboard_to_board,
    board_to_bitboard,
    get_empty_positions_bitboard,
    set_cell_exponent,
    validate_bitboard,
)

TWO_PROBABILITY = 0.9
FOUR_PROBABILITY = 0.1


def choose_new_tile_value(rng: Optional[random.Random] = None) -> int:
    rng = rng or random
    return 2 if rng.random() < TWO_PROBABILITY else 4


def _choose_new_tile_exponent(rng: Optional[random.Random] = None) -> int:
    return 1 if choose_new_tile_value(rng) == 2 else 2


def spawn_random_tile_bitboard(bitboard: BitBoard, rng: Optional[random.Random] = None) -> BitBoard:
    validate_bitboard(bitboard)
    rng = rng or random

    empty_positions = get_empty_positions_bitboard(bitboard)
    if not empty_positions:
        return bitboard

    idx = rng.choice(empty_positions)
    exp = _choose_new_tile_exponent(rng)
    return set_cell_exponent(bitboard, idx, exp)


def spawn_random_tile(board: Union[Board, BitBoard], rng: Optional[random.Random] = None) -> Union[Board, BitBoard]:
    rng = rng or random

    if isinstance(board, int):
        return spawn_random_tile_bitboard(board, rng)

    bitboard = board_to_bitboard(board)
    spawned = spawn_random_tile_bitboard(bitboard, rng)
    return bitboard_to_board(spawned)


def create_initial_bitboard(rng: Optional[random.Random] = None) -> BitBoard:
    rng = rng or random
    bitboard = 0
    bitboard = spawn_random_tile_bitboard(bitboard, rng)
    bitboard = spawn_random_tile_bitboard(bitboard, rng)
    return bitboard


def create_initial_board(rng: Optional[random.Random] = None) -> Board:
    return bitboard_to_board(create_initial_bitboard(rng))
from __future__ import annotations

import random
from typing import Optional

from .board import Board, copy_board, get_empty_cells, validate_board

TWO_PROBABILITY = 0.9
FOUR_PROBABILITY = 0.1


def choose_new_tile_value(rng: Optional[random.Random] = None) -> int:
    """
    Return the value of a newly spawned tile.

    By default:
    - 2 with probability 0.9
    - 4 with probability 0.1
    """
    rng = rng or random
    return 2 if rng.random() < TWO_PROBABILITY else 4


def spawn_random_tile(board: Board, rng: Optional[random.Random] = None) -> Board:
    """
    Return a new board with one random tile (2 or 4) placed
    in a random empty cell.

    If the board has no empty cells, returns a copy unchanged.
    """
    validate_board(board)
    rng = rng or random

    new_board = copy_board(board)
    empty_cells = get_empty_cells(new_board)

    if not empty_cells:
        return new_board

    row, col = rng.choice(empty_cells)
    new_board[row][col] = choose_new_tile_value(rng)

    return new_board


def create_initial_board(rng: Optional[random.Random] = None) -> Board:
    """
    Create a fresh board with two random starting tiles.
    """
    from .board import create_empty_board

    rng = rng or random
    board = create_empty_board()
    board = spawn_random_tile(board, rng)
    board = spawn_random_tile(board, rng)
    return board
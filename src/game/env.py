from __future__ import annotations

from typing import Any, Dict, Optional, Tuple
import random

from .board import Board, BitBoard, bitboard_to_board
from .logic import apply_move_bitboard, get_legal_moves
from .spawn import create_initial_bitboard, spawn_random_tile_bitboard
from .state import get_max_tile, get_score_after_move, has_won, is_game_over


StepResult = Tuple[Board, int, bool, Dict[str, Any]]
BitStepResult = Tuple[BitBoard, int, bool, Dict[str, Any]]


class Game2048Env:
    def __init__(self, target: int = 2048, rng: Optional[random.Random] = None) -> None:
        self.target = target
        self.rng = rng or random.Random()
        self.board: BitBoard = 0
        self.score: int = 0
        self.done: bool = False
        self.won: bool = False
        self.move_count: int = 0
        self.reset_bitboard()

    def reset(self) -> Board:
        return bitboard_to_board(self.reset_bitboard())

    def reset_bitboard(self) -> BitBoard:
        self.board = create_initial_bitboard(self.rng)
        self.score = 0
        self.done = False
        self.won = False
        self.move_count = 0
        return self.board

    def get_state(self) -> Board:
        return bitboard_to_board(self.board)

    def get_bitboard_state(self) -> BitBoard:
        return self.board

    def get_score(self) -> int:
        return self.score

    def get_move_count(self) -> int:
        return self.move_count

    def get_max_tile(self) -> int:
        return get_max_tile(self.board)

    def get_legal_moves(self) -> list[str]:
        return get_legal_moves(self.board)

    def step(self, action: str) -> StepResult:
        next_board, reward, done, info = self.step_bitboard(action)
        return bitboard_to_board(next_board), reward, done, info

    def step_bitboard(self, action: str) -> BitStepResult:
        if self.done:
            raise RuntimeError("Cannot call step() after game is over. Call reset() first.")

        new_board, reward, changed = apply_move_bitboard(self.board, action)

        if changed:
            self.score = get_score_after_move(self.score, reward)
            self.board = spawn_random_tile_bitboard(new_board, self.rng)
            self.move_count += 1
        else:
            self.board = new_board

        self.won = has_won(self.board, self.target)
        self.done = is_game_over(self.board)
        legal_moves = [] if self.done else get_legal_moves(self.board)

        info: Dict[str, Any] = {
            "changed": changed,
            "score": self.score,
            "max_tile": get_max_tile(self.board),
            "won": self.won,
            "move_count": self.move_count,
            "legal_moves": legal_moves,
        }

        return self.board, reward, self.done, info
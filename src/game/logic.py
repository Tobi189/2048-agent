from __future__ import annotations

from typing import List, Tuple, Union

from .board import (
    Board,
    BitBoard,
    bitboard_to_board,
    board_to_bitboard,
    validate_bitboard,
    validate_board,
)

MoveResult = Tuple[Board, int, bool]
BitMoveResult = Tuple[BitBoard, int, bool]
VALID_MOVES = {"left", "right", "up", "down"}


def compress_line_left(line: List[int]) -> List[int]:
    non_zero = [value for value in line if value != 0]
    zeros = [0] * (len(line) - len(non_zero))
    return non_zero + zeros


def merge_line_left(line: List[int]) -> Tuple[List[int], int]:
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
    compressed = compress_line_left(line)
    merged, reward = merge_line_left(compressed)
    return merged, reward


def _copy_board(board: Board) -> Board:
    return [row[:] for row in board]


def _reverse_rows(board: Board) -> Board:
    return [list(reversed(row)) for row in board]


def _transpose_board(board: Board) -> Board:
    return [list(row) for row in zip(*board)]


def _move_left_board(board: Board) -> MoveResult:
    validate_board(board)

    new_board: Board = []
    total_reward = 0

    for row in board:
        new_row, reward = process_line_left(row)
        new_board.append(new_row)
        total_reward += reward

    changed = new_board != board
    return new_board, total_reward, changed


def _move_right_board(board: Board) -> MoveResult:
    validate_board(board)

    reversed_board = _reverse_rows(board)
    moved_board, reward, _ = _move_left_board(reversed_board)
    restored_board = _reverse_rows(moved_board)

    changed = restored_board != board
    return restored_board, reward, changed


def _move_up_board(board: Board) -> MoveResult:
    validate_board(board)

    transposed = _transpose_board(board)
    moved_board, reward, _ = _move_left_board(transposed)
    restored_board = _transpose_board(moved_board)

    changed = restored_board != board
    return restored_board, reward, changed


def _move_down_board(board: Board) -> MoveResult:
    validate_board(board)

    transposed = _transpose_board(board)
    moved_board, reward, _ = _move_right_board(transposed)
    restored_board = _transpose_board(moved_board)

    changed = restored_board != board
    return restored_board, reward, changed


def move_left_bitboard(bitboard: BitBoard) -> BitMoveResult:
    validate_bitboard(bitboard)
    board = bitboard_to_board(bitboard)
    moved_board, reward, changed = _move_left_board(board)
    return board_to_bitboard(moved_board), reward, changed


def move_right_bitboard(bitboard: BitBoard) -> BitMoveResult:
    validate_bitboard(bitboard)
    board = bitboard_to_board(bitboard)
    moved_board, reward, changed = _move_right_board(board)
    return board_to_bitboard(moved_board), reward, changed


def move_up_bitboard(bitboard: BitBoard) -> BitMoveResult:
    validate_bitboard(bitboard)
    board = bitboard_to_board(bitboard)
    moved_board, reward, changed = _move_up_board(board)
    return board_to_bitboard(moved_board), reward, changed


def move_down_bitboard(bitboard: BitBoard) -> BitMoveResult:
    validate_bitboard(bitboard)
    board = bitboard_to_board(bitboard)
    moved_board, reward, changed = _move_down_board(board)
    return board_to_bitboard(moved_board), reward, changed


def apply_move_bitboard(bitboard: BitBoard, direction: str) -> BitMoveResult:
    validate_bitboard(bitboard)

    direction = direction.lower().strip()
    if direction not in VALID_MOVES:
        raise ValueError(f"Invalid move '{direction}'. Valid moves: {sorted(VALID_MOVES)}")

    if direction == "left":
        return move_left_bitboard(bitboard)
    if direction == "right":
        return move_right_bitboard(bitboard)
    if direction == "up":
        return move_up_bitboard(bitboard)
    return move_down_bitboard(bitboard)


def move_left(board: Union[Board, BitBoard]) -> Union[MoveResult, BitMoveResult]:
    if isinstance(board, int):
        return move_left_bitboard(board)

    validate_board(board)
    return _move_left_board(_copy_board(board))


def move_right(board: Union[Board, BitBoard]) -> Union[MoveResult, BitMoveResult]:
    if isinstance(board, int):
        return move_right_bitboard(board)

    validate_board(board)
    return _move_right_board(_copy_board(board))


def move_up(board: Union[Board, BitBoard]) -> Union[MoveResult, BitMoveResult]:
    if isinstance(board, int):
        return move_up_bitboard(board)

    validate_board(board)
    return _move_up_board(_copy_board(board))


def move_down(board: Union[Board, BitBoard]) -> Union[MoveResult, BitMoveResult]:
    if isinstance(board, int):
        return move_down_bitboard(board)

    validate_board(board)
    return _move_down_board(_copy_board(board))


def apply_move(board: Union[Board, BitBoard], direction: str) -> Union[MoveResult, BitMoveResult]:
    if isinstance(board, int):
        return apply_move_bitboard(board, direction)

    validate_board(board)

    direction = direction.lower().strip()
    if direction not in VALID_MOVES:
        raise ValueError(f"Invalid move '{direction}'. Valid moves: {sorted(VALID_MOVES)}")

    if direction == "left":
        return _move_left_board(_copy_board(board))
    if direction == "right":
        return _move_right_board(_copy_board(board))
    if direction == "up":
        return _move_up_board(_copy_board(board))
    return _move_down_board(_copy_board(board))


def has_legal_moves(board: Union[Board, BitBoard]) -> bool:
    if isinstance(board, int):
        validate_bitboard(board)
        for direction in ("left", "right", "up", "down"):
            _, _, changed = apply_move_bitboard(board, direction)
            if changed:
                return True
        return False

    validate_board(board)

    for direction in ("left", "right", "up", "down"):
        _, _, changed = apply_move(board, direction)
        if changed:
            return True
    return False


def get_legal_moves(board: Union[Board, BitBoard]) -> List[str]:
    if isinstance(board, int):
        validate_bitboard(board)
        legal_moves: List[str] = []
        for direction in ("left", "right", "up", "down"):
            _, _, changed = apply_move_bitboard(board, direction)
            if changed:
                legal_moves.append(direction)
        return legal_moves

    validate_board(board)

    legal_moves: List[str] = []
    for direction in ("left", "right", "up", "down"):
        _, _, changed = apply_move(board, direction)
        if changed:
            legal_moves.append(direction)
    return legal_moves
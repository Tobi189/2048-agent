from __future__ import annotations

from typing import List, Tuple, Union

from .board import (
    Board,
    BitBoard,
    validate_bitboard,
    validate_board,
)

MoveResult = Tuple[Board, int, bool]
BitMoveResult = Tuple[BitBoard, int, bool]
VALID_MOVES = {"left", "right", "up", "down"}

ROW_MASK = 0xFFFF
NIBBLE_MASK = 0xF


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


def _pack_row(exponents: List[int]) -> int:
    return sum((exp & NIBBLE_MASK) << (4 * i) for i, exp in enumerate(exponents))


def _reverse_row(row: int) -> int:
    return (
        ((row & 0x000F) << 12)
        | ((row & 0x00F0) << 4)
        | ((row & 0x0F00) >> 4)
        | ((row & 0xF000) >> 12)
    )


def _process_row_left_exponents(row: int) -> Tuple[int, int]:
    tiles = [(row >> (4 * i)) & NIBBLE_MASK for i in range(4)]
    non_zero = [value for value in tiles if value != 0]

    merged: List[int] = []
    reward = 0
    i = 0
    while i < len(non_zero):
        if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
            new_exp = non_zero[i] + 1
            merged.append(new_exp)
            reward += 1 << new_exp
            i += 2
        else:
            merged.append(non_zero[i])
            i += 1

    merged.extend([0] * (4 - len(merged)))
    return _pack_row(merged), reward


_ROW_LEFT_RESULT = [0] * 65536
_ROW_LEFT_REWARD = [0] * 65536
_ROW_RIGHT_RESULT = [0] * 65536
_ROW_RIGHT_REWARD = [0] * 65536

for _row in range(65536):
    _left_result, _left_reward = _process_row_left_exponents(_row)
    _ROW_LEFT_RESULT[_row] = _left_result
    _ROW_LEFT_REWARD[_row] = _left_reward

for _row in range(65536):
    _reversed_row = _reverse_row(_row)
    _right_result_reversed = _ROW_LEFT_RESULT[_reversed_row]
    _ROW_RIGHT_RESULT[_row] = _reverse_row(_right_result_reversed)
    _ROW_RIGHT_REWARD[_row] = _ROW_LEFT_REWARD[_reversed_row]


def _extract_row(bitboard: BitBoard, row_idx: int) -> int:
    return (bitboard >> (16 * row_idx)) & ROW_MASK


def _extract_column_as_row(bitboard: BitBoard, col_idx: int) -> int:
    shift = 4 * col_idx
    return (
        ((bitboard >> shift) & NIBBLE_MASK)
        | (((bitboard >> (16 + shift)) & NIBBLE_MASK) << 4)
        | (((bitboard >> (32 + shift)) & NIBBLE_MASK) << 8)
        | (((bitboard >> (48 + shift)) & NIBBLE_MASK) << 12)
    )


def _write_column_from_row(bitboard: BitBoard, col_idx: int, row_value: int) -> BitBoard:
    shift = 4 * col_idx
    mask = (
        (NIBBLE_MASK << shift)
        | (NIBBLE_MASK << (16 + shift))
        | (NIBBLE_MASK << (32 + shift))
        | (NIBBLE_MASK << (48 + shift))
    )
    updates = (
        ((row_value & NIBBLE_MASK) << shift)
        | (((row_value >> 4) & NIBBLE_MASK) << (16 + shift))
        | (((row_value >> 8) & NIBBLE_MASK) << (32 + shift))
        | (((row_value >> 12) & NIBBLE_MASK) << (48 + shift))
    )
    return (bitboard & ~mask) | updates


def move_left_bitboard(bitboard: BitBoard) -> BitMoveResult:
    validate_bitboard(bitboard)

    new_bitboard = 0
    reward = 0
    for row_idx in range(4):
        row = _extract_row(bitboard, row_idx)
        moved_row = _ROW_LEFT_RESULT[row]
        reward += _ROW_LEFT_REWARD[row]
        new_bitboard |= moved_row << (16 * row_idx)

    changed = new_bitboard != bitboard
    return new_bitboard, reward, changed


def move_right_bitboard(bitboard: BitBoard) -> BitMoveResult:
    validate_bitboard(bitboard)

    new_bitboard = 0
    reward = 0
    for row_idx in range(4):
        row = _extract_row(bitboard, row_idx)
        moved_row = _ROW_RIGHT_RESULT[row]
        reward += _ROW_RIGHT_REWARD[row]
        new_bitboard |= moved_row << (16 * row_idx)

    changed = new_bitboard != bitboard
    return new_bitboard, reward, changed


def move_up_bitboard(bitboard: BitBoard) -> BitMoveResult:
    validate_bitboard(bitboard)

    new_bitboard = bitboard
    reward = 0
    for col_idx in range(4):
        column = _extract_column_as_row(bitboard, col_idx)
        moved_column = _ROW_LEFT_RESULT[column]
        reward += _ROW_LEFT_REWARD[column]
        new_bitboard = _write_column_from_row(new_bitboard, col_idx, moved_column)

    changed = new_bitboard != bitboard
    return new_bitboard, reward, changed


def move_down_bitboard(bitboard: BitBoard) -> BitMoveResult:
    validate_bitboard(bitboard)

    new_bitboard = bitboard
    reward = 0
    for col_idx in range(4):
        column = _extract_column_as_row(bitboard, col_idx)
        moved_column = _ROW_RIGHT_RESULT[column]
        reward += _ROW_RIGHT_REWARD[column]
        new_bitboard = _write_column_from_row(new_bitboard, col_idx, moved_column)

    changed = new_bitboard != bitboard
    return new_bitboard, reward, changed


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


list_move_left = _move_left_board
list_move_right = _move_right_board
list_move_up = _move_up_board
list_move_down = _move_down_board
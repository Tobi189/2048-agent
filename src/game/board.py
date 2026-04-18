from __future__ import annotations

from typing import List, Tuple

Board = List[List[int]]
Position = Tuple[int, int]

BOARD_SIZE = 4


def create_empty_board(size: int = BOARD_SIZE) -> Board:
    """
    Create an empty square board filled with zeros.

    Args:
        size: Board width/height. Defaults to 4.

    Returns:
        A size x size board filled with 0.
    """
    if size <= 0:
        raise ValueError("Board size must be a positive integer.")

    return [[0 for _ in range(size)] for _ in range(size)]


def copy_board(board: Board) -> Board:
    """
    Return a deep copy of the board.

    Args:
        board: 2D board list.

    Returns:
        A new board with copied rows.
    """
    validate_board(board)
    return [row[:] for row in board]


def get_empty_cells(board: Board) -> List[Position]:
    """
    Return coordinates of all empty cells (cells containing 0).

    Args:
        board: 2D board list.

    Returns:
        List of (row, col) tuples for empty cells.
    """
    validate_board(board)

    empty_cells: List[Position] = []
    for row_idx, row in enumerate(board):
        for col_idx, value in enumerate(row):
            if value == 0:
                empty_cells.append((row_idx, col_idx))

    return empty_cells


def get_board_size(board: Board) -> int:
    """
    Return the size of a square board.

    Args:
        board: 2D board list.

    Returns:
        Board size.
    """
    validate_board(board)
    return len(board)


def print_board(board: Board) -> None:
    """
    Pretty-print the board to the console.

    Empty cells are shown as dots for readability.

    Args:
        board: 2D board list.
    """
    validate_board(board)

    cell_width = max(4, max(len(str(value)) for row in board for value in row if value != 0) if any(
        value != 0 for row in board for value in row
    ) else 4)

    horizontal = "+" + "+".join(["-" * cell_width for _ in range(len(board))]) + "+"

    print(horizontal)
    for row in board:
        formatted_row = []
        for value in row:
            display = "." if value == 0 else str(value)
            formatted_row.append(display.rjust(cell_width))
        print("|" + "|".join(formatted_row) + "|")
        print(horizontal)


def validate_board(board: Board) -> None:
    """
    Validate that the board is a non-empty square 2D list of integers.

    Args:
        board: Object expected to be a board.

    Raises:
        ValueError: If board structure is invalid.
        TypeError: If cell values are not integers.
    """
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


if __name__ == "__main__":
    board = create_empty_board()
    print("Empty board:")
    print_board(board)

    board[0][0] = 2
    board[1][2] = 4

    print("\nModified board:")
    print_board(board)

    print("\nEmpty cells:", get_empty_cells(board))
    print("Copied board:", copy_board(board))
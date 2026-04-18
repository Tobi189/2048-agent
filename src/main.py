from game.board import print_board
from game.logic import apply_move, get_legal_moves, has_legal_moves
from game.spawn import create_initial_board, spawn_random_tile

MOVE_MAP = {
    "w": "up",
    "a": "left",
    "s": "down",
    "d": "right",
}


def main() -> None:
    current_board = create_initial_board()

    while True:
        print("\nCurrent board:")
        print_board(current_board)

        legal_moves = get_legal_moves(current_board)
        print("Legal moves:", legal_moves)

        if not has_legal_moves(current_board):
            print("Game over.")
            break

        user_input = input("Enter move (w/a/s/d) or q to quit: ").strip().lower()

        if user_input == "q":
            print("Exiting.")
            break

        if user_input not in MOVE_MAP:
            print("Invalid input.")
            continue

        direction = MOVE_MAP[user_input]
        new_board, reward, changed = apply_move(current_board, direction)

        print(f"Move: {direction}")
        print(f"Reward gained: {reward}")
        print(f"Board changed: {changed}")

        if changed:
            current_board = spawn_random_tile(new_board)
        else:
            print("That move does nothing.")


if __name__ == "__main__":
    main()
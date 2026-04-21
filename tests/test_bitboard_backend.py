import random
import unittest

from src.game.board import (
    bitboard_to_board,
    board_to_bitboard,
)
from src.game.env import Game2048Env
from src.game.logic import (
    apply_move,
    apply_move_bitboard,
    get_legal_moves,
    has_legal_moves,
)
from src.game.spawn import (
    create_initial_bitboard,
    create_initial_board,
    spawn_random_tile,
    spawn_random_tile_bitboard,
)
from src.game.state import (
    get_max_tile,
    has_won,
    is_game_over,
)


TEST_TILE_VALUES = [
    0, 2, 4, 8, 16, 32, 64, 128,
    256, 512, 1024, 2048, 4096,
]


def random_board(rng: random.Random):
    return [
        [rng.choice(TEST_TILE_VALUES) for _ in range(4)]
        for _ in range(4)
    ]


class TestBitboardBackend(unittest.TestCase):
    def test_roundtrip_random_boards(self):
        rng = random.Random(12345)

        for _ in range(200):
            board = random_board(rng)
            bitboard = board_to_bitboard(board)
            restored = bitboard_to_board(bitboard)
            self.assertEqual(restored, board)

    def test_apply_move_bitboard_matches_list_random_boards(self):
        rng = random.Random(222)

        for _ in range(200):
            board = random_board(rng)
            bitboard = board_to_bitboard(board)

            for direction in ("left", "right", "up", "down"):
                with self.subTest(board=board, direction=direction):
                    expected_board, expected_reward, expected_changed = apply_move(board, direction)
                    got_bitboard, got_reward, got_changed = apply_move_bitboard(bitboard, direction)
                    got_board = bitboard_to_board(got_bitboard)

                    self.assertEqual(got_board, expected_board)
                    self.assertEqual(got_reward, expected_reward)
                    self.assertEqual(got_changed, expected_changed)

    def test_apply_move_does_not_mutate_original_board(self):
        board = [
            [2, 0, 2, 4],
            [0, 4, 4, 0],
            [2, 2, 2, 0],
            [0, 0, 0, 2],
        ]
        original = [row[:] for row in board]

        for direction in ("left", "right", "up", "down"):
            _ = apply_move(board, direction)
            self.assertEqual(board, original)

    def test_legal_moves_match_random_boards(self):
        rng = random.Random(333)

        for _ in range(200):
            board = random_board(rng)
            bitboard = board_to_bitboard(board)

            with self.subTest(board=board):
                self.assertEqual(get_legal_moves(board), get_legal_moves(bitboard))
                self.assertEqual(has_legal_moves(board), has_legal_moves(bitboard))

    def test_state_helpers_match_random_boards(self):
        rng = random.Random(444)

        for _ in range(200):
            board = random_board(rng)
            bitboard = board_to_bitboard(board)

            with self.subTest(board=board):
                self.assertEqual(get_max_tile(board), get_max_tile(bitboard))
                self.assertEqual(has_won(board), has_won(bitboard))
                self.assertEqual(is_game_over(board), is_game_over(bitboard))

    def test_spawn_random_tile_bitboard_matches_list_with_same_seed(self):
        rng_boards = random.Random(555)

        for seed in range(100):
            board = random_board(rng_boards)

            rng1 = random.Random(seed)
            rng2 = random.Random(seed)

            spawned_list = spawn_random_tile(board, rng1)
            spawned_bit = spawn_random_tile_bitboard(board_to_bitboard(board), rng2)
            spawned_bit_as_board = bitboard_to_board(spawned_bit)

            with self.subTest(seed=seed, board=board):
                self.assertEqual(spawned_bit_as_board, spawned_list)

    def test_create_initial_bitboard_matches_create_initial_board_same_seed(self):
        for seed in range(100):
            rng1 = random.Random(seed)
            rng2 = random.Random(seed)

            board1 = create_initial_board(rng1)
            board2 = bitboard_to_board(create_initial_bitboard(rng2))

            with self.subTest(seed=seed):
                self.assertEqual(board1, board2)

    def test_full_board_spawn_is_unchanged_in_both_backends(self):
        board = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [2, 4, 8, 16],
        ]

        rng1 = random.Random(777)
        rng2 = random.Random(777)

        spawned_list = spawn_random_tile(board, rng1)
        spawned_bit = spawn_random_tile_bitboard(board_to_bitboard(board), rng2)

        self.assertEqual(spawned_list, board)
        self.assertEqual(bitboard_to_board(spawned_bit), board)

    def test_env_produces_only_valid_tiles_over_many_steps(self):
        env = Game2048Env(rng=random.Random(888))
        valid_values = {0} | {2 ** k for k in range(1, 16)}

        for _ in range(200):
            board = env.get_state()

            for row in board:
                self.assertEqual(len(row), 4)
                for value in row:
                    self.assertIn(value, valid_values)

            if env.done:
                break

            legal = env.get_legal_moves()
            if not legal:
                break

            action = legal[0]
            board, reward, done, info = env.step(action)

            self.assertIsInstance(reward, int)
            self.assertIsInstance(done, bool)
            self.assertIsInstance(info, dict)

    def test_env_and_manual_play_stay_in_sync_for_fixed_policy(self):
        seed = 999
        env = Game2048Env(rng=random.Random(seed))

        manual_rng = random.Random(seed)
        manual_board = create_initial_board(manual_rng)
        manual_score = 0

        for _ in range(50):
            env_board = env.get_state()
            self.assertEqual(env_board, manual_board)
            self.assertEqual(env.get_score(), manual_score)

            legal = get_legal_moves(manual_board)
            if not legal:
                self.assertTrue(env.done or is_game_over(env_board))
                break

            action = legal[0]

            env_board_after, env_reward, env_done, _ = env.step(action)

            new_manual_board, manual_reward, changed = apply_move(manual_board, action)
            if changed:
                manual_score += manual_reward
                manual_board = spawn_random_tile(new_manual_board, manual_rng)
            else:
                manual_board = new_manual_board

            self.assertEqual(env_reward, manual_reward)
            self.assertEqual(env_board_after, manual_board)

            if env_done:
                break


if __name__ == "__main__":
    unittest.main()
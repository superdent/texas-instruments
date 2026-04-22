import unittest
from vierti import *

class TestBoard(unittest.TestCase):
    def test_create_board_shape(self):
        board = create_board()
        self.assertEqual(len(board), 6)
        self.assertTrue(all(len(row) == 7 for row in board))

    def test_apply_move_drops_to_bottom(self):
        board = create_board()
        row = apply_move(board, 3, PLAYER_ONE)
        self.assertEqual(row, 5)
        self.assertEqual(board[5][3], PLAYER_ONE)

    def test_apply_move_raises_when_column_full(self):
        board = create_board()
        for _ in range(6):
            apply_move(board, 0, PLAYER_ONE)
        with self.assertRaises(ValueError):
            apply_move(board, 0, PLAYER_ONE)

    def test_undo_move_removes_top_piece(self):
        board = create_board()
        apply_move(board, 0, PLAYER_ONE)
        apply_move(board, 0, PLAYER_TWO)
        row = undo_move(board, 0)
        self.assertEqual(row, 4)
        self.assertEqual(board[4][0], CELL_EMPTY)
        self.assertEqual(board[5][0], PLAYER_ONE)

    def test_get_valid_columns_excludes_full_column(self):
        board = create_board()
        for _ in range(6):
            apply_move(board, 0, PLAYER_ONE)
        self.assertNotIn(0, get_valid_columns(board))
        self.assertIn(1, get_valid_columns(board))

    def test_has_winner_horizontal(self):
        board = create_board()
        for col in range(4):
            apply_move(board, col, PLAYER_ONE)
        self.assertEqual(has_winner(board), PLAYER_ONE)

    def test_has_winner_vertical(self):
        board = create_board()
        for _ in range(4):
            apply_move(board, 2, PLAYER_TWO)
        self.assertEqual(has_winner(board), PLAYER_TWO)

    def test_has_winner_diagonal_down_right(self):
        board = create_board()
        apply_move(board, 0, PLAYER_ONE)

        apply_move(board, 1, PLAYER_TWO)
        apply_move(board, 1, PLAYER_ONE)

        apply_move(board, 2, PLAYER_TWO)
        apply_move(board, 2, PLAYER_TWO)
        apply_move(board, 2, PLAYER_ONE)

        apply_move(board, 3, PLAYER_TWO)
        apply_move(board, 3, PLAYER_TWO)
        apply_move(board, 3, PLAYER_TWO)
        apply_move(board, 3, PLAYER_ONE)

        # print_board(board)
        self.assertEqual(has_winner(board), PLAYER_ONE)

    def test_is_full_false_on_empty_board(self):
        board = create_board()
        self.assertFalse(is_full(board))

    def test_is_full_true_on_full_board(self):
        board = create_board()
        for col in range(7):
            for _ in range(6):
                apply_move(board, col, PLAYER_ONE)
        self.assertTrue(is_full(board))

if __name__ == "__main__":
    unittest.main()

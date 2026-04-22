import random

CELL_EMPTY = 0
PLAYER_ONE = 1
PLAYER_TWO = 2

def create_board():
    return [[CELL_EMPTY for _ in range(7)] for _ in range(6)]

def apply_move(board, col, current_player):
    if col < 0 or col > 6:
        raise ValueError("col")
    for row in range(5, -1, -1):
        if board[row][col] == CELL_EMPTY:
            board[row][col] = current_player
            return row
    raise ValueError("column full")

def undo_move(board, col):
    for row in range(6):
        if board[row][col] != CELL_EMPTY:
            board[row][col] = CELL_EMPTY
            return row
    raise ValueError("column empty")

def get_valid_columns(board):
    valid_columns = []
    for col in range(7):
        if board[0][col] == CELL_EMPTY:
            valid_columns.append(col)
    return valid_columns

def has_winner(board):
    winner = has_winner_horizontal(board)
    if winner != CELL_EMPTY:
        return winner
    winner = has_winner_vertical(board)
    if winner != CELL_EMPTY:
        return winner
    winner = has_winner_diagonal(board)
    if winner != CELL_EMPTY:
        return winner
    return CELL_EMPTY

def has_winner_horizontal(board):
    for row in range(6):
        for col in range(4):
            cell = board[row][col]
            if cell != CELL_EMPTY and \
               cell == board[row][col + 1] and \
               cell == board[row][col + 2] and \
               cell == board[row][col + 3]:
                return cell
    return CELL_EMPTY

def has_winner_vertical(board):
    for col in range(7):
        for row in range(3):
            cell = board[row][col]
            if cell != CELL_EMPTY and \
               cell == board[row + 1][col] and \
               cell == board[row + 2][col] and \
               cell == board[row + 3][col]:
                return cell
    return CELL_EMPTY

def has_winner_diagonal(board):
    for row in range(3):
        for col in range(4):
            cell = board[row][col]
            if cell != CELL_EMPTY and \
               cell == board[row + 1][col + 1] and \
               cell == board[row + 2][col + 2] and \
               cell == board[row + 3][col + 3]:
                return cell

    for row in range(3):
        for col in range(3, 7):
            cell = board[row][col]
            if cell != CELL_EMPTY and \
               cell == board[row + 1][col - 1] and \
               cell == board[row + 2][col - 2] and \
               cell == board[row + 3][col - 3]:
                return cell

    return CELL_EMPTY

def is_full(board):
    for col in range(7):
        if board[0][col] == CELL_EMPTY:
            return False
    return True

def print_board(board):
    for row in board:
        print(" ".join(str(x) for x in row))

def run_two_player_game():
    board = create_board()
    current_player = PLAYER_ONE

    while True:
        print_board(board)
        col = int(input("Spalte (0-6): "))
        apply_move(board, col, current_player)

        winner = has_winner(board)
        if winner != CELL_EMPTY:
            print_board(board)
            print("Gewinner:", winner)
            return

        if is_full(board):
            print_board(board)
            print("Unentschieden")
            return

        if current_player == PLAYER_ONE:
            current_player = PLAYER_TWO
        else:
            current_player = PLAYER_ONE

def choose_ai_column(board):
    valid_columns = get_valid_columns(board)
    return random.choice(valid_columns)

def run_human_vs_ai_game():
    board = create_board()
    current_player = random.choice([PLAYER_ONE, PLAYER_TWO])

    while True:
        print_board(board)

        if current_player == PLAYER_ONE:
            col = int(input("Spalte (0-6): "))
        else:
            col = choose_ai_column(board)
            print("KI waehlt:", col)

        apply_move(board, col, current_player)

        winner = has_winner(board)
        if winner != CELL_EMPTY:
            print_board(board)
            print("Gewinner:", winner)
            return

        if is_full(board):
            print_board(board)
            print("Unentschieden")
            return

        if current_player == PLAYER_ONE:
            current_player = PLAYER_TWO
        else:
            current_player = PLAYER_ONE

if __name__ == "__main__":
    run_human_vs_ai_game()
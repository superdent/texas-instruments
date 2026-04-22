import random

CELL_EMPTY = 0
PLAYER_ONE = 1
PLAYER_TWO = 2

tk_root = None
tk_canvas = None

DISPLAY_MODE = "tkinter"  # "text" oder "ti_draw oder "tkinter"

CELL_CHARS = {CELL_EMPTY: ".", PLAYER_ONE: "X", PLAYER_TWO: "O"}

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

def print_board_text(board):
    for row in board:
        print(" ".join(CELL_CHARS[x] for x in row))
    print("0 1 2 3 4 5 6")


def tk_init():
    global tk_root, tk_canvas
    import tkinter as tk
    CELL_SIZE = 80
    MARGIN = 10
    tk_root = tk.Tk()
    tk_root.title("Vierti")
    tk_canvas = tk.Canvas(tk_root, width=7*CELL_SIZE+2*MARGIN, height=6*CELL_SIZE+2*MARGIN, bg="#333333")
    tk_canvas.pack()

def print_board_tkinter(board):
    global tk_root, tk_canvas
    import tkinter as tk
    CELL_SIZE = 80
    MARGIN = 10
    COLORS = {CELL_EMPTY: "#cccccc", PLAYER_ONE: "#dd3333", PLAYER_TWO: "#3333dd"}
    if tk_root is None:
        tk_init()
    tk_canvas.delete("all")
    for row in range(6):
        for col in range(7):
            x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
            y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
            r = CELL_SIZE // 2 - 5
            tk_canvas.create_oval(x-r, y-r, x+r, y+r, fill=COLORS[board[row][col]], outline="")
    tk_root.update()

def print_board_ti_draw(board):
    try:
        import ti_draw
        ti_draw.clear()
        cell_size = 20
        for row in range(6):
            for col in range(7):
                x = col * cell_size + 5
                y = row * cell_size + 5
                cell = board[row][col]
                if cell == CELL_EMPTY:
                    ti_draw.set_color(128, 128, 128)
                elif cell == PLAYER_ONE:
                    ti_draw.set_color(220, 50, 50)
                else:
                    ti_draw.set_color(50, 50, 220)
                ti_draw.fill_circle(x + cell_size // 2, y + cell_size // 2, cell_size // 2 - 2)
        ti_draw.show_draw()
    except ImportError:
        print_board_text(board)

def print_board(board):
    if DISPLAY_MODE == "ti_draw":
        print_board_ti_draw(board)
    elif DISPLAY_MODE == "tkinter":
        print_board_tkinter(board)
    else:
        print_board_text(board)

def score_window(window, player):
    opp = PLAYER_ONE if player == PLAYER_TWO else PLAYER_TWO
    p = window.count(player)
    e = window.count(CELL_EMPTY)
    o = window.count(opp)
    if p == 4:
        return 100
    if p == 3 and e == 1:
        return 5
    if p == 2 and e == 2:
        return 2
    if o == 3 and e == 1:
        return -4
    return 0

def score_board(board, player):
    score = 0
    center = [board[r][3] for r in range(6)]
    score += center.count(player) * 3
    for r in range(6):
        for c in range(4):
            w = [board[r][c+i] for i in range(4)]
            score += score_window(w, player)
    for r in range(3):
        for c in range(7):
            w = [board[r+i][c] for i in range(4)]
            score += score_window(w, player)
    for r in range(3):
        for c in range(4):
            w = [board[r+i][c+i] for i in range(4)]
            score += score_window(w, player)
    for r in range(3, 6):
        for c in range(4):
            w = [board[r-i][c+i] for i in range(4)]
            score += score_window(w, player)
    return score

def minimax(board, depth, alpha, beta, maximizing, ai_player):
    opp = PLAYER_ONE if ai_player == PLAYER_TWO else PLAYER_TWO
    winner = has_winner(board)
    if winner == ai_player:
        return (None, 10000 + depth)
    if winner == opp:
        return (None, -10000 - depth)
    if is_full(board) or depth == 0:
        return (None, score_board(board, ai_player))
    cols = get_valid_columns(board)
    best_col = cols[len(cols) // 2]
    if maximizing:
        value = -99999
        for col in cols:
            apply_move(board, col, ai_player)
            _, score = minimax(board, depth-1, alpha, beta, False, ai_player)
            undo_move(board, col)
            if score > value:
                value = score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (best_col, value)
    else:
        value = 99999
        for col in cols:
            apply_move(board, col, opp)
            _, score = minimax(board, depth-1, alpha, beta, True, ai_player)
            undo_move(board, col)
            if score < value:
                value = score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (best_col, value)

def get_ai_move(board, ai_player, depth=3):
    col, _ = minimax(board, depth, -99999, 99999, True, ai_player)
    return col

def choose_ai_column(board):
    return get_ai_move(board, PLAYER_TWO)

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
            print("Gewinner:", CELL_CHARS[winner])
            return
        if is_full(board):
            print_board(board)
            print("Unentschieden")
            return
        current_player = PLAYER_TWO if current_player == PLAYER_ONE else PLAYER_ONE

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
            print("Gewinner:", CELL_CHARS[winner])
            return
        if is_full(board):
            print_board(board)
            print("Unentschieden")
            return
        current_player = PLAYER_TWO if current_player == PLAYER_ONE else PLAYER_ONE

if __name__ == "__main__":
    run_human_vs_ai_game()
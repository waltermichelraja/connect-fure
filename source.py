ROWS=8
COLUMNS=8
EMPTY='.'
PLAYER_SYMBOLS=['X', 'O']


def create_board():
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    print("\n  "+" ".join(str(i) for i in range(COLUMNS)))
    for row in board:
        print(" |"+"|".join(row)+"|")
    print()

def is_valid_column(board, col):
    return 0<=col<COLUMNS and board[0][col]==EMPTY

def get_next_open_row(board, col):
    for row in reversed(range(ROWS)):
        if board[row][col]==EMPTY:
            return row
    return None

def drop_piece(board, row, col, piece):
    board[row][col]=piece

def is_draw(board):
    return all(board[0][col]!=EMPTY for col in range(COLUMNS))


def win_condition(board, piece):
    pass # to do...
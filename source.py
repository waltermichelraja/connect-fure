ROWS=8
COLUMNS=8
EMPTY="."
PLAYER_SYMBOLS=["X", "O"]


def create_board():
    return [[EMPTY for _ in range(COLUMNS)] for i in range(ROWS)]

def print_board(board):
    print("\n "+" ".join(str(i+1) for i in range(COLUMNS)))
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
    """c=1
    while c<4:
        if(board[row][col]==piece):
            c+=1
            row-=1
        elif row==0 or board[row][col]!=piece:
            return False""" # col => [to be passed -> ()]

    for r in range(ROWS):
        for c in range(COLUMNS-3):
            if (board[r][c]==piece and
                board[r][c+1]==piece and
                board[r][c+2]==piece and
                board[r][c+3]==piece):
                return True # horizontal

    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if (board[r][c]==piece and
                board[r+1][c]==piece and
                board[r+2][c]==piece and
                board[r+3][c]==piece):
                return True # vertical

        

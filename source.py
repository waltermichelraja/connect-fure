ROWS=8
COLUMNS=8
EMPTY=["1","2","3","4","5","6","7","8"]
PLAYER_SYMBOLS=['X', 'O']


def create_board():
    return [[EMPTY[i] for _ in range(COLUMNS)] for i in range(ROWS)]

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
            return row#this one
    return None

def drop_piece(board, row, col, piece):
    board[row][col]=piece

def is_draw(board):
    return all(board[0][col]!=EMPTY for col in range(COLUMNS))


def win_condition(board, piece):
    #for vertical here i use that row for easy access also in this func i need the col of user input
    c=1
    while c<4:
        if(board[row][col]==piece):
            c+=1
            row-=1
        elif row==0 or board[row][col]!=piece:
            return False
    if c==4 cout<<player won return
        

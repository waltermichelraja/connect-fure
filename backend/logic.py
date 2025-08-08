import uuid

ROWS=8
COLUMNS=8
EMPTY="."
PLAYER_SYMBOLS=["X", "O"]

STATUS_IN_PROGRESS=1
STATUS_GAME_OVER=0
STATUS_DRAW=-1


class User:
    def __init__(self, username):
        self.id=str(uuid.uuid4())
        self.username=username
        self.games=[]


class Connect4:
    def __init__(self, player_id1, player_id2):
        self.id=str(uuid.uuid4())
        self.players=[player_id1, player_id2]
        self.reset_board()

    def reset_board(self):
        self.board=[[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.turn=0
        self.winner=None
        self.status=STATUS_IN_PROGRESS
        self.move_history=[]

    def is_valid_column(self, col):
        return 0 <=col < COLUMNS and self.board[0][col]==EMPTY

    def get_next_open_row(self, col):
        for row in reversed(range(ROWS)):
            if self.board[row][col]==EMPTY:
                return row
        return None

    def drop_piece(self, row, col, piece):
        self.board[row][col]=piece

    def is_draw(self):
        return all(self.board[0][col] !=EMPTY for col in range(COLUMNS))

    def win_condition(self, piece):
        for r in range(ROWS):
            for c in range(COLUMNS - 3):
                if all(self.board[r][c+i]==piece for i in range(4)):
                    return True

        for c in range(COLUMNS):
            for r in range(ROWS - 3):
                if all(self.board[r+i][c]==piece for i in range(4)):
                    return True

        for r in range(ROWS - 3):
            for c in range(COLUMNS - 3):
                if all(self.board[r+i][c+i]==piece for i in range(4)):
                    return True

        for r in range(ROWS - 3):
            for c in range(3, COLUMNS):
                if all(self.board[r+i][c-i]==piece for i in range(4)):
                    return True

        return False

    def play(self, player_id, col):
        if self.status !=STATUS_IN_PROGRESS:
            return False, "game already finished"
        if self.players[self.turn%2]!=player_id:
            return False, "not your turn"
        if not self.is_valid_column(col):
            return False, "invalid column"

        row=self.get_next_open_row(col)
        piece=PLAYER_SYMBOLS[self.turn%2]
        self.drop_piece(row, col, piece)
        self.move_history.append((row, col, player_id))

        if self.win_condition(piece):
            self.status=STATUS_GAME_OVER
            self.winner=player_id
        elif self.is_draw():
            self.status=STATUS_DRAW
        else:
            self.turn+=1

        return True, "move played"

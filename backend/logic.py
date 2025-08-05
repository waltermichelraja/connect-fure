ROWS=8
COLUMNS=8
EMPTY="."
PLAYER_SYMBOLS=["X", "O"]

class GameLogic:
    def __init__(self):
        self.board=[[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.turn=0
        self.winner=None

    def is_valid_column(self, col):
        return 0<=col<COLUMNS and self.board[0][col]==EMPTY

    def get_next_open_row(self, col):
        for row in reversed(range(ROWS)):
            if self.board[row][col]==EMPTY:
                return row
        return None

    def drop_piece(self, row, col, piece):
        self.board[row][col]=piece

    def is_draw(self):
        return all(self.board[0][col]!=EMPTY for col in range(COLUMNS))

    def win_condition(self, piece):
        for r in range(ROWS):
            for c in range(COLUMNS-3):
                if all(self.board[r][c+i]==piece for i in range(4)):
                    return True

        for c in range(COLUMNS):
            for r in range(ROWS-3):
                if all(self.board[r+i][c]==piece for i in range(4)):
                    return True

        for r in range(ROWS-3):
            for c in range(COLUMNS-3):
                if all(self.board[r+i][c+i]==piece for i in range(4)):
                    return True

        for r in range(ROWS-3):
            for c in range(3, COLUMNS):
                if all(self.board[r+i][c-i]==piece for i in range(4)):
                    return True

        return False
    
    def play(self, col):
        pass #to do....
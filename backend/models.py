import uuid

ROWS=8
COLUMNS=8
EMPTY="."
PLAYER_SYMBOLS=["X", "O"]
STATUS_IN_PROGRESS=1
STATUS_DRAW=0
STATUS_GAME_OVER=-1

class User:
    def __init__(self, email, username, password):
        self.id=str(uuid.uuid4())
        self.email=email
        self.username=username
        self.password=password
        self.games=[]
    
    def to_dict(self):
        return {
            "_id": self.id,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "games": self.games
        }

class Connect4:
    def __init__(self, player1_id, player2_id, board=None, turn=0,
                 status=STATUS_IN_PROGRESS, move_history=None, winner=None, game_id=None):
        self.id=game_id or str(uuid.uuid4())
        self.players=[player1_id, player2_id]
        self.board=board or [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.turn=turn
        self.status=status
        self.move_history=move_history or []
        self.winner=winner

    @classmethod
    def from_dict(cls, data):
        return cls(
            player1_id=data["players"][0],
            player2_id=data["players"][1],
            board=data["board"],
            turn=data["turn"],
            status=data["status"],
            move_history=data.get("move_history", []),
            winner=data.get("winner"),
            game_id=data.get("_id")
        )

    def to_dict(self):
        return {
            "_id": self.id,
            "players": self.players,
            "board": self.board,
            "turn": self.turn,
            "status": self.status,
            "move_history": self.move_history,
            "winner": self.winner
        }

    def reset_board(self):
        self.board=[[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.turn=0
        self.status=STATUS_IN_PROGRESS
        self.move_history=[]
        self.winner=None

    def is_valid_column(self, col):
        return 0<=col<COLUMNS and self.board[0][col]==EMPTY

    def get_next_open_row(self, col):
        for r in range(ROWS-1, -1, -1):
            if self.board[r][col]==EMPTY:
                return r
        return None

    def drop_piece(self, row, col, piece):
        self.board[row][col]=piece

    def check_winner(self, piece):
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

        for r in range(3, ROWS):
            for c in range(COLUMNS-3):
                if all(self.board[r-i][c+i]==piece for i in range(4)):
                    return True
        return False

    def is_board_full(self):
        return all(self.board[0][c]!=EMPTY for c in range(COLUMNS))

    def play(self, player_id, col):
        if self.status!=STATUS_IN_PROGRESS:
            return False, "game already finished"
        if self.players[self.turn%2]!=player_id:
            return False, "not your turn."
        if not self.is_valid_column(col):
            return False, "invalid column."
        
        row=self.get_next_open_row(col)
        if row is None:
            return False, "column is full."

        piece="X" if self.turn%2==0 else "O"
        self.drop_piece(row, col, piece)
        self.move_history.append((player_id, col))

        if self.check_winner(piece):
            self.status=STATUS_GAME_OVER
            self.winner=player_id
            return True, f"player {player_id} wins!"

        if self.is_board_full():
            self.status=STATUS_DRAW
            return True, "game is a draw!"
        self.turn+=1
        return True, "move successful!"

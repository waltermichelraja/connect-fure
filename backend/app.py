from flask import Flask, request, jsonify
from logic import Connect4, User, PLAYER_SYMBOLS, STATUS_IN_PROGRESS

app=Flask(__name__)

games={}  # {game_id: Connect4}
users={}  # {user_id: User}


@app.route("/")
def root():
    return {"author": "Walter Michel Raja JR", "email": "waltermichelraja@gmail.com"}


@app.route("/user", methods=["POST"])
def create_user():
    username=request.json.get("username")
    if not username:
        return {"error": "username required"}, 400

    user=User(username)
    users[user.id]=user
    return {"id": user.id, "username": user.username}


@app.route("/game", methods=["POST"])
def create_game():
    data=request.json
    p1=data.get("player1_id")
    p2=data.get("player2_id")

    if not (p1 and p2):
        return {"error": "both player IDs required"}, 400
    if p1 not in users or p2 not in users:
        return {"error": "invalid player ID(s)"}, 400
    game=Connect4(p1, p2)
    games[game.id]=game
    users[p1].games.append(game.id)
    users[p2].games.append(game.id)

    return game_state(game)


@app.route("/game/<game_id>", methods=["GET"])
def fetch_game(game_id):
    game=games.get(game_id)
    if not game:
        return {"error": "game not found"}, 404
    return game_state(game)


@app.route("/game/<game_id>/play", methods=["POST"])
def play_game(game_id):
    game=games.get(game_id)
    if not game:
        return {"error": "game not found"}, 404

    data=request.json
    player_id=data.get("player_id")
    col=data.get("column")

    if player_id not in users:
        return {"error": "invalid player ID"}, 400
    if col is None:
        return {"error": "column required"}, 400

    success, message=game.play(player_id, col)
    if not success:
        return {"error": message}, 400

    return game_state(game, message)


@app.route("/game/<game_id>/restart", methods=["POST"])
def restart_game(game_id):
    game=games.get(game_id)
    if not game:
        return {"error": "game not found"}, 404

    game.reset_board()
    return game_state(game, "game restarted")


def game_state(game, message=None):
    return {
        "id": game.id,
        "board": game.board,
        "turn": game.turn,
        "current_player_id": game.players[game.turn%2],
        "current_player_symbol": PLAYER_SYMBOLS[game.turn%2],
        "winner": game.winner,
        "status": game.status,
        "move_history": game.move_history,
        **({"message": message} if message else {})
    }


if __name__=="__main__":
    app.run(debug=True)

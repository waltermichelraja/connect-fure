from flask import Flask, request
from logic import Connect4, User, PLAYER_SYMBOLS
import logging

app=Flask(__name__)

games={}  # {game_id: Connect4}
users={}  # {user_id: User}

logging.basicConfig(level=logging.INFO)

@app.route("/")
def root():
    return {
        "author": "Walter Michel Raja JR",
        "email": "waltermichelraja@gmail.com"
    }


@app.route("/user", methods=["POST"])
def create_user():
    username=request.json.get("username")
    if not username:
        return error_response("username required", 400)

    user=User(username)
    users[user.id]=user
    logging.info(f"user created: {username} ({user.id})")
    return {"id": user.id, "username": user.username}


@app.route("/game", methods=["POST"])
def create_game():
    data=request.json
    p1=data.get("player1_id")
    p2=data.get("player2_id")

    if not (p1 and p2):
        return error_response("both player IDs required", 400)
    if p1 not in users or p2 not in users:
        return error_response("invalid player ID(s)", 400)

    game = Connect4(p1, p2)
    games[game.id]=game
    users[p1].games.append(game.id)
    users[p2].games.append(game.id)

    logging.info(f"game created: {game.id} between {p1} and {p2}")
    return game_state(game)


@app.route("/game/<game_id>", methods=["GET"])
def fetch_game(game_id):
    game=games.get(game_id)
    if not game:
        return error_response("game not found", 404)
    return game_state(game)


@app.route("/game/<game_id>/play", methods=["POST"])
def play_game(game_id):
    game=games.get(game_id)
    if not game:
        return error_response("game not found", 404)

    data=request.json
    player_id=data.get("player_id")
    try:
        col=int(data.get("column"))
    except (ValueError, TypeError):
        return error_response("column must be an integer", 400)

    if player_id not in users:
        return error_response("invalid player ID", 400)

    success, message=game.play(player_id, col)
    if not success:
        return error_response(message, 400)

    logging.info(f"move: player {player_id} in game {game_id} => column {col}")
    return game_state(game, message)


@app.route("/game/<game_id>/restart", methods=["POST"])
def restart_game(game_id):
    game=games.get(game_id)
    if not game:
        return error_response("game not found", 404)

    game.reset_board()
    logging.info(f"game restarted: {game_id}")
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


def error_response(message, status):
    return {"error": message}, status


if __name__ == "__main__":
    app.run(debug=True)

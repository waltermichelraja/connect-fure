from flask import Flask, request, jsonify
from logic import Connect4, PLAYER_SYMBOLS

app=Flask(__name__)
games=dict() # {}
users=dict() # {}

@app.route("/")
def root():
    return {"author": "walter michel raja", "email":"waltermichelraja@gmail.com"}

@app.route("/game", methods=["POST"])
def create_game():
    game=Connect4()
    games[game.id]=game
    return jsonify({
        "id": game.id,
        "board": game.board,
        "turn": game.turn,
        "current_player": PLAYER_SYMBOLS[game.turn%2],
        "winner": game.winner,
        "status": game.status
    })

@app.route("/game/<game_id>", methods=["GET"])
def fetch_game(game_id):
    game=games.get(game_id)
    if not game:
        return jsonify({"error": "game not found"}), 404
    return jsonify({
        "id": game.id,
        "board": game.board,
        "turn": game.turn,
        "current_player": PLAYER_SYMBOLS[game.turn%2],
        "winner": game.winner,
        "status": game.status
    })

@app.route("/game/<game_id>/play", methods=["POST"])
def play_game(game_id):
    game=games.get(game_id)
    if not game:
        return jsonify({"error": "game not found"}), 404
    data=request.json
    if "column" not in data:
        return jsonify({"error": "column required"}), 400
    success, message=game.play(data["column"])
    if not success:
        return jsonify({"error": message}), 400
    return jsonify({
        "board": game.board,
        "turn": game.turn,
        "current_player": PLAYER_SYMBOLS[game.turn%2],
        "winner": game.winner,
        "status": game.status
    })

@app.route("/game/<game_id>/restart", methods=["POST"])
def restart_game(game_id):
    game=games.get(game_id)
    if not game:
        return jsonify({"error": "game not found"}), 404
    game.__init__()
    games[game.id]=game
    return jsonify({"message": "game restarted", "board": game.board})


if __name__=="__main__":
    app.run(debug=True)
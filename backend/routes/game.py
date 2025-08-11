from flask import Blueprint, request
from models import Connect4
from dump import games, users
from utils import *
import logging

game_bp=Blueprint("game", __name__)

@game_bp.route("/game", methods=["POST"])
def create_game():
    data=request.json
    p1=data.get("player1_id")
    p2=data.get("player2_id")

    if not (p1 and p2):
        return error_response("both player IDs required", 400)
    if p1 not in users or p2 not in users:
        return error_response("invalid player ID(s)", 400)

    game=Connect4(p1, p2)
    games[game.id]=game
    users[p1].games.append(game.id)
    users[p2].games.append(game.id)

    logging.info(f"game created: {game.id} between {p1} and {p2}")
    return game_state(game)

@game_bp.route("/game/<game_id>", methods=["GET"])
def fetch_game(game_id):
    game=games.get(game_id)
    if not game:
        return error_response("game not found", 404)
    return game_state(game)

@game_bp.route("/game/<game_id>/play", methods=["POST"])
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

@game_bp.route("/game/<game_id>/restart", methods=["POST"])
def restart_game(game_id):
    game=games.get(game_id)
    if not game:
        return error_response("game not found", 404)

    game.reset_board()
    logging.info(f"game restarted: {game_id}")
    return game_state(game, "game restarted")

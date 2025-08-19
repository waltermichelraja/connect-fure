from flask import Blueprint, request
from models import Connect4
from db import games_collection, users_collection
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

    if not users_collection.find_one({"_id": p1}) or not users_collection.find_one({"_id": p2}) or p1==p2:
        return error_response("invalid player ID(s)", 400)

    game=Connect4(p1, p2)
    games_collection.insert_one(game.to_dict())
    users_collection.update_one({"_id": p1}, {"$push": {"games": game.id}})
    users_collection.update_one({"_id": p2}, {"$push": {"games": game.id}})

    logging.info(f"game created: {game.id} between {p1} and {p2}")
    #log_to_db() -> activate at production
    return game_state(game)


@game_bp.route("/game/<game_id>", methods=["GET"])
def fetch_game(game_id):
    game_doc=games_collection.find_one({"_id": game_id})
    if not game_doc:
        return error_response("game not found", 404)

    game=Connect4.from_dict(game_doc)
    return game_state(game)


@game_bp.route("/game/<game_id>/play", methods=["POST"])
def play_game(game_id):
    game_doc=games_collection.find_one({"_id": game_id})
    if not game_doc:
        return error_response("game not found", 404)

    data=request.json
    player_id=data.get("player_id")
    try:
        col=int(data.get("column"))
    except(ValueError, TypeError):
        return error_response("column must be an integer", 400)

    if not users_collection.find_one({"_id": player_id}):
        return error_response("invalid player ID", 400)

    game=Connect4.from_dict(game_doc)
    success, message=game.play(player_id, col)
    if not success:
        return error_response(message, 400)
    
    games_collection.update_one(
        {"_id": game.id},
        {"$set": {
            "board": game.board,
            "turn": game.turn,
            "winner": game.winner,
            "status": game.status,
            "move_history": game.move_history
        }}
    )
    if game.status==-1:
        if game.winner:
            users_collection.update_one(
                {"_id": game.winner},
                {"$inc": {"wins": 1}}
            )
            loser=[p for p in game.players if p!=game.winner][0]
            users_collection.update_one(
                {"_id": loser},
                {"$inc": {"losses": 1}}
            )
        else:
            for p in game.players:
                users_collection.update_one(
                    {"_id": p},
                    {"$inc": {"draws": 1}}
                )
    logging.info(f"move: player {player_id} [{col}] in game {game_id}")
    #log_to_db() -> activate at production
    return game_state(game, message)


@game_bp.route("/game/<game_id>/restart", methods=["POST"])
def restart_game(game_id):
    game_doc=games_collection.find_one({"_id": game_id})
    if not game_doc:
        return error_response("game not found", 404)

    game=Connect4.from_dict(game_doc)
    game.reset_board()
    games_collection.update_one(
        {"_id": game.id},
        {"$set": {
            "board": game.board,
            "turn": game.turn,
            "winner": game.winner,
            "status": game.status,
            "move_history": game.move_history
        }}
    )
    logging.info(f"game restarted: {game_id}")
    #log_to_db() -> activate at production
    return game_state(game, "game restarted")

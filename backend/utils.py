from models import PLAYER_SYMBOLS

def error_response(message, status):
    return {"error": message}, status

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

import re
import dns.resolver
from werkzeug.security import generate_password_hash
from db import users_collection
from models import PLAYER_SYMBOLS

EMAIL_PATTERN=re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
USERNAME_PATTERN=re.compile(r'^[A-Za-z_][A-Za-z0-9_]{5,15}$')

def is_valid_email_format(email):
    if not EMAIL_PATTERN.match(email):
        return False, "invalid email format."
    return True, None
def is_unique_email(email):
    if users_collection.find_one({"email": email}):
        return False, "email already registered."
    return True, None
def email_domain_has_mx(email):
    domain=email.split('@')[-1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True, None
    except dns.resolver.NoAnswer:
        return False, "email domain has no mail server."
    except dns.resolver.NXDOMAIN:
        return False, "email domain does not exist."
    except Exception:
        return False, "error verifying email domain."

def is_valid_username(username):
    if not username or not USERNAME_PATTERN.match(username):
        return False, "follow the username contraints."
    return True, None
def is_unique_username(username):
    if users_collection.find_one({"username": username}):
        return False, "username already exists."
    return True, None

def is_valid_password(password):
    if not password:
        return False, "follow the password constraints."
    if len(password)<6 or len(password)>16:
        return False, "password must be between 6-16 characters."
    return True, None
def hash_password(password):
    return generate_password_hash(password)

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

from flask import Blueprint, request
from models import User
from dump import users
from utils import *
import logging

user_bp=Blueprint("user", __name__)

@user_bp.route("/user", methods=["POST"])
def create_user():
    username=request.json.get("username")
    if not username:
        return error_response("username required", 400)

    user=User(username)
    users[user.id]=user
    logging.info(f"user created: {username} ({user.id})")
    return {"id": user.id, "username": user.username}

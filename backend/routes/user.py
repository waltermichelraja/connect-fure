from flask import Blueprint, request
from models import User
from db import users_collection
from utils import *
import logging

user_bp=Blueprint("user", __name__)
users_collection.create_index("email", unique=True)
users_collection.create_index("username", unique=True)

@user_bp.route("/user", methods=["POST"])
def create_user():
    data=request.json
    email=data.get("email")
    username=data.get("username")
    password=data.get("password")

    if not username:
        return error_response("username required", 400)
    if not email:
        return error_response("email required", 400)
    if not password:
        return error_response("password required", 400)
    
    valid, msg=is_valid_username(username)
    if not valid:
        return error_response(msg, 400)
    unique, msg=is_unique_username(username)
    if not unique:
        return error_response(msg, 400)
    
    valid, msg=is_valid_email_format(email)
    if not valid:
        return error_response(msg, 400)
    unique, msg=is_unique_email(email)
    if not unique:
        return error_response(msg, 400)
    domain_ok, msg=email_domain_has_mx(email)
    if not domain_ok:
        return error_response(msg, 400)

    valid, msg=is_valid_password(password)
    if not valid:
        return error_response(msg, 400)

    hashed_pw=hash_password(password)
    user=User(email, username, hashed_pw)
    users_collection.insert_one(user.to_dict())

    logging.info(f"user created: {username} [{user.id}] with email {email}")
    return {
        "id": user.id,
        "email": email,
        "username": user.username,
        "message": "user created successfully."
    }
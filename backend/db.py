from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI=os.getenv("MONGO_URI")
if not MONGO_URI:
    raise EnvironmentError("MONGO_URI environment variable not set")

client=MongoClient(MONGO_URI)
db=client["connectfure_db"]

users_collection=db["users"]
games_collection=db["games"]
logs_collection = db["logs"]

users_collection.create_index("email", unique=True)
users_collection.create_index("username", unique=True)
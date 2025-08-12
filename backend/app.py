from flask import Flask
import logging
from routes.user import user_bp
from routes.game import game_bp

app=Flask(__name__)

logging.basicConfig(level=logging.INFO)

app.register_blueprint(user_bp)
app.register_blueprint(game_bp)

@app.route("/")
def root():
    return {
        "author": "Walter Michel Raja JR",
        "email": "waltermichelraja@gmail.com"
    }

if __name__=="__main__":
    app.run(debug=True)

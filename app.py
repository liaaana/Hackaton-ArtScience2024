import numpy as np
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "Sbjbdkcdkv762BSvfedJDV3"
socketio = SocketIO(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = ""
from routes import *
def runApp():
    with app.app_context():
        db.create_all()
    app.run("0.0.0.0", port=1233, debug=True)

if __name__ == "__main__":
   runApp()


@socketio.on("connect")
def test_connect():
    print("Socket successfully connected")
    emit("my response", {"data": "Connected"})





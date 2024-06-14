import numpy as np
from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "Sbjbdkcdkv762BSvfedJDV3"
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

from routes import *


def runApp():
    app.run("0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    runApp()

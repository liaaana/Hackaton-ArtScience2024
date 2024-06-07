import base64
import json

import cv2
import numpy as np
from flask import Response, render_template, request, redirect, url_for, flash
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask import stream_with_context, request
from flask_socketio import emit
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, Response

from exersices import Exercises
from forms.login_form import LoginForm
from forms.register_form import RegistrationForm
from app import app, db, login_manager, socketio
from models.user import User

def base64_to_image(base64_string):
    # Extract the base64 encoded binary data from the input string
    base64_data = base64_string.split(",")[1]
    # Decode the base64 data to bytes
    image_bytes = base64.b64decode(base64_data)
    # Convert the bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode the numpy array as an image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


def load_translations(language):
    translations = {}
    try:
        with open(f'translations/{language}.json', 'r', encoding='utf-8') as file:
            translations = json.load(file)
    except FileNotFoundError:
        pass
    return translations


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/rating")
def rating():
    users = (
        User.query.order_by(User.exercise1_counter + User.exercise2_counter).all()
    )

    users = users[::-1]
    return render_template("rating.html", users=users)


@app.route("/exercises")
def exercisesPage():
    return render_template("exercises.html")


@app.route("/curl_preview")
@login_required
def curl_preview():
    """Video streaming squat page."""
    return render_template("curl_preview.html")


@app.route("/curl")
@login_required
def curl():
    """Video streaming squat page."""
    return render_template("curl.html")


@app.route("/push_up_preview")
@login_required
def push_up_preview():
    return render_template("push_up_preview.html")


@app.route("/push_up")
@login_required
def push_up():
    """Video streaming squat page."""
    return render_template("push_up.html")


@app.route("/squat_preview")
@login_required
def squat_preview():
    return render_template("squat_preview.html")


@app.route("/squat")
@login_required
def squat():
    """Video streaming squat page."""
    return render_template("squat.html")


currentExercise = ""

exercises = Exercises()
@socketio.on("exercise")
def receive_exersice(exercise):
    exercises.counter = 0
    exercises.stage = None
    global currentExercise
    currentExercise = exercise


@socketio.on("image")
def receive_image(image):

    image = base64_to_image(image)
    img = None
    if (currentExercise == "squat"):
        img = exercises.gen_squat(image)
    elif (currentExercise == "push_up"):
        img = exercises.gen_push_up(image)
    elif (currentExercise == "curl"):
        img = exercises.gen_curl(image)

    if img is None: return
    processed_img_data = base64.b64encode(img).decode()
    # Prepend the base64-encoded string with the data URL prefix
    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data
    # Send the processed image back to the client

    emit("processed_image", processed_img_data)



@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html", form=form)




@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("profile"))
        else:
            flash("Invalid email or password", "danger")
    return render_template("login.html", form=form)


@app.route('/profile')
@login_required
def profile():
    user_language = current_user.language
    translations = load_translations(user_language)
    return render_template('profile.html', user=current_user, translations=translations)


@app.route("/change_username", methods=["POST"])
@login_required
def change_username():
    new_name = request.form.get("new_name")
    if new_name:
        current_user.name = new_name
        db.session.commit()
    return redirect("/profile")


@app.route("/change_language", methods=["POST"])
@login_required
def change_language():
    new_language = request.form.get("new_language")
    if new_language:
        current_user.language = new_language
        db.session.commit()
    return redirect("/profile")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


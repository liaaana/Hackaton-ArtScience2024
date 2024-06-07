from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    exercise1_counter = db.Column(db.Integer, default=0)
    exercise2_counter = db.Column(db.Integer, default=0)
    exercise3_counter = db.Column(db.Integer, default=0)
    exercise4_counter = db.Column(db.Integer, default=0)
    exercise5_counter = db.Column(db.Integer, default=0)
    language = db.Column(db.String(5), nullable=False, default="ru")

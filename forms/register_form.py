from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length


class RegistrationForm(FlaskForm):
    name = StringField(
        "Name", validators=[InputRequired(), Length(min=4, max=20)]
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(message="Invalid email"), Length(max=50)],
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=6, max=80)]
    )
    submit = SubmitField("Register")

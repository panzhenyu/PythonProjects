from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, SubmitField

class login(FlaskForm):
    user_name = StringField()
    password = PasswordField()
    submit = SubmitField()
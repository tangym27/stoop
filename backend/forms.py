from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms.widgets import PasswordInput

from app import db


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[
                           DataRequired()], widget=PasswordInput(hide_value=False))
    submit = SubmitField("Login")


class SignupForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[DataRequired(), Length(
        min=6)], widget=PasswordInput(hide_value=False))
    passwordConfirm = StringField("Confirm Password", validators=[DataRequired(
    ), Length(min=6), EqualTo("password")], widget=PasswordInput(hide_value=False))
    firstName = StringField("First Name", validators=[DataRequired()])
    lastName = StringField("Last Name", validators=[DataRequired()])
    submit = SubmitField("Register")

    # automatically validates on the `email` field because it's called `validate_email`
    def validate_email(self, email):
        user = db.users.find_one({"email": email})
        if user:
            raise ValidationError(
                "An account under this email address has already been created.")

import datetime
import pymongo
import urllib.parse
from pymongo import MongoClient
from flask import Flask, render_template, flash, request, session, redirect, url_for, jsonify
from datetime import datetime
import json
from bson import json_util

app = Flask(__name__)

# must run python3 -m pip install 'pymongo[srv]'
# documentation: https://pymongo.readthedocs.io/en/stable/tutorial.html
app.config['SECRET_KEY'] = "KIUYGY(H't76$A%U$6"
googleAPIKey = "AIzaSyBbRW0nz9TJyiBTA-DrZbve8nc9m0viXBU"
client = MongoClient(
    "mongodb+srv://admin:ibqamgEqZgrWoEJP@cluster0.j7aiy.mongodb.net/stoop?retryWrites=true&w=majority")
global db
db = client.stoop
users = db.users
volunteers = db.volunteers
requests = db.requests

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms.widgets import PasswordInput


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
    # def validate_email(self, email):
    #     user = users.find({"email": email})
    #     if user:
    #         raise ValidationError(
    #             "An account under this email address has already been created.")

class RequestForm(FlaskForm):
    category = RadioField('Category', choices=[('delivery','delivery'),('social','social'), ('other', 'other')])
    task = StringField("Task", validators=[DataRequired()])
    address = StringField("Address")
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Request")

    # def validate_address(self, address):
    #     if category == "delivery" and not address:
    #         raise ValidationError("Address is required for delivery")

@app.route("/")
def home():
    return redirect(url_for("dashboard"))

# see recent orders
@app.route("/dashboard")
def dashboard():
    # seeing your own orders
    # { user: session.get("user").get("id") }
    # seeing orders you accepted
    # { volunteer: session.get("user").get("id") }
    if not session.get("user"):
        return redirect(url_for("login"))
    
    allRequests = []
    for request in requests.find({}):
        _id = str(request.get("_id"))
        task = request.get("task")
        category = request.get("category")
        description = request.get("description")
        dateRequested = request.get("dateRequested")
        finished = request.get("finished")
        volunteer = request.get("volunteer")
        print(volunteer)
        
        requestObj = {
            "_id": _id,
            "task": task,
            "category": category,
            "description": description,
            "dateRequested": str(dateRequested).split(" ")[0],
            "finished": finished
        }
        allRequests.append(requestObj)
    
    return render_template("dashboard.html", requests={"requests": allRequests})

@app.route("/claim", methods=["POST"])
def claim():
    if not session.get("user"):
        return redirect(url_for("login"))

    requestID = request.form.get("requestID")
    userID = session.get("user").get("id")

    requests.update_one({ "_id": requestID}, { "$set": { "volunteer": userID } })
    flash("You have successfully claimed this task", "success")
    return redirect(url_for("dashboard"))

# @app.route("/complete", methods=["POST"])
# def complete():
#     if not session.get("user"):
#         return redirect(url_for("login"))

#     requestID = request.form.get("requestID")
#     userID = session.get("user").get("id")

#     requests.update_one({ "_id": requestID}, { "$set": { "finished": True } })
#     flash("You have successfully completed this task", "success")
#     return redirect(url_for("dashboard"))

# submitting a request
@app.route('/requestOne', methods=['POST', 'GET'])
def requestOne():
    if not session.get("user"):
        return redirect(url_for("login"))

    requestForm = RequestForm()

    if requestForm.validate_on_submit():
        task = request.form.get("task")
        category = request.form.get("category")
        description = request.form.get("description")

        request_dicts= {
            "task": task,
            "user": session.get("user").get("id"),
            "volunteer": None,
            "category": category,
            "description": description,
            "dateRequested": datetime.now(),
            "finished": False,
        }

        requests.insert_one(request_dicts)
        return redirect(url_for("dashboard"))
    return render_template("request.html", requestForm = requestForm)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if session.get("user"):
        return redirect(url_for("dashboard"))

    signupForm = SignupForm()
    if signupForm.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')

        # # check if user in database already
        # if users.find_one({"email": email}):
        #     loginForm = LoginForm()
        #     return render_template("login.html", loginForm=loginForm)

        new_user = {"email": email, "password": password,
                    "first_name": first_name, "last_name": last_name}
        new_user_id = str(users.insert_one(new_user))
        session["user"] = {"email": email, "first_name": first_name, "last_name": last_name, "id": new_user_id}
        flash("You have successfully signed up and logged in", "success")
    return render_template("signup.html", signupForm=signupForm)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get("user"):
        return redirect(url_for("dashboard"))

    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')

        # check if user in database
        user = users.find_one({"email": email})

        if user and password == user.get('password'):
            session["user"] = {"email": email, "first_name": user.get("first_name"), "last_name": user.get("last_name"),"id": user.get("_id")}
            flash("You have successfully logged in", "success")
            return redirect(url_for("dashboard"))
    
    return render_template("login.html", loginForm=loginForm)

@app.route('/logout')
def logout():
    session.pop("user")
    return redirect(url_for("home"))

if __name__ == "__main__":
    # print(users.find_one({"id": 0}))
    # print(volunteers.find_one({"id": 0}))
    # print(requests.find_one({"id": 0}))
    app.debug = True
    app.run()

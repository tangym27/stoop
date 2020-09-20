import datetime
import pymongo
import urllib.parse
import requests as rq
from geopy import distance
from pymongo import MongoClient
from flask import Flask, render_template, flash, request, session, redirect, url_for, jsonify
from datetime import datetime
import json
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

# must run python3 -m pip install 'pymongo[srv]'
# documentation: https://pymongo.readthedocs.io/en/stable/tutorial.html
app.config['SECRET_KEY'] = "KIUYGY(H't76$A%U$6"
# googleAPIKey = "AIzaSyBbRW0nz9TJyiBTA-DrZbve8nc9m0viXBU"
googleAPIKey = "AIzaSyC3MU7FGVapAnAKEsN48cu4sLG2ITQd33E"
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
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address"})
    password = StringField("Password", validators=[
                DataRequired()], widget=PasswordInput(hide_value=False), render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")
    
class SignupForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address"})
    password = StringField("Password", validators=[DataRequired(), Length(
        min=6)], widget=PasswordInput(hide_value=False), render_kw={"placeholder": "Password"})
    passwordConfirm = StringField("Confirm Password", validators=[DataRequired(
    ), Length(min=6), EqualTo("password")], widget=PasswordInput(hide_value=False), render_kw={"placeholder": "Confirm Password"})
    firstName = StringField("First Name", validators=[DataRequired()], render_kw={"placeholder": "First Name"})
    lastName = StringField("Last Name", validators=[DataRequired()], render_kw={"placeholder": "Last Name"})
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
    #     if not address:
    #         raise ValidationError("Address is required for delivery")
    #     try: 
    #         rq.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&key=' + googleAPIKey).content
    #         return True
    #     except:
    #         raise ValidationError("Address invalid")

class AddressForm(FlaskForm):
    address = StringField("Address", validators=[DataRequired()], render_kw={"placeholder": "Address"})
    submit = SubmitField("Find Requests")


@app.route("/")
def home():
    return redirect(url_for("dashboard"))

# see recent orders
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if not session.get("user"):
        return redirect(url_for("login"))
    
    requestType = request.args.get("requests")
    requestType = requestType if requestType else "allRequests"
    # myRequests
    # myClaimedRequests
    # all
    allRequests = []
    toSort = []
    idx = 0
    addressForm = AddressForm()
    volunteerLocation = None
    volunteercoords = None
    
    if addressForm.validate_on_submit():
        try:
            address = request.form.get("address")
            volunteerLocation = rq.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&key=' + googleAPIKey).content
            volunteercoords = json.loads(volunteerLocation)["results"][0]["geometry"]["location"]
            volunteercoords = (volunteercoords["lat"], volunteercoords["lng"])
        except:
            flash(address + " is an invalid address", "danger")
            return render_template("dashboard.html", addressForm = addressForm, requests={"requests": allRequests}, requestType=requestType)
    
    for req in requests.find({}).sort("dateRequested",pymongo.DESCENDING):
        _id = str(req.get("_id"))
        user = str(req.get("user"))
        task = req.get("task")
        category = req.get("category")
        description = req.get("description")
        dateRequested = req.get("dateRequested")
        finished = req.get("finished")
        volunteer = req.get("volunteer")
        address = req.get("address")

        # calculate distance using google maps api
        location = rq.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + str(address) + '&key=' + googleAPIKey).content

        coords = json.loads(location)["results"][0]["geometry"]["location"]
        coords = (coords["lat"], coords["lng"])

        # user_location = session.get('location')

        requestObj = {
                "_id": _id,
                "task": task,
                "category": category,
                "description": description,
                "dateRequested": str(dateRequested).split(" ")[0],
                "finished": finished,
                "volunteer": volunteer,
                "user": user,
                "address": address,
                "distance": "N/A" if not volunteercoords else round(distance.distance(coords, volunteercoords).miles, 4)
        }

        if requestType=="myRequests" and user == session.get("user").get("id"):
            allRequests.append(requestObj)

        elif requestType=="myClaimedRequests" and volunteer == session.get("user").get("id"):
            allRequests.append(requestObj)

        elif requestType=="allRequests" and (not volunteer or user == session.get("user").get("id") or volunteer == session.get("user").get("id")):
            if volunteerLocation:
                if distance.distance(coords, volunteercoords).miles < 10:
                    allRequests.append(requestObj)
                    toSort.append((distance.distance(coords, volunteercoords), idx))
                    idx += 1
    sortedReqs = sorted(toSort)
    sortedAllRequests = []
    for sortedReq in sortedReqs:
        sortedAllRequests.append(allRequests[sortedReq[1]])

    if len(sortedAllRequests) == 0:
        sortedAllRequests = allRequests
    return render_template("dashboard.html", addressForm = addressForm, requests={"requests": sortedAllRequests}, requestType=requestType)

@app.route("/claim", methods=["POST"])
def claim():
    if not session.get("user"):
        return redirect(url_for("login"))

    requestID = request.form.get("requestID")
    userID = session.get("user").get("id")
    requestID = requestID[1:-1]
    requests.update_one({ "_id": ObjectId(requestID)}, { "$set": { "volunteer": userID } })

    flash("You have successfully claimed this task", "success")
    return redirect(url_for("dashboard"))

@app.route("/complete", methods=["POST"])
def complete():
    if not session.get("user"):
        return redirect(url_for("login"))

    requestID = request.form.get("requestID")
    requestID = requestID[1:-1]
    requests.update_one({ "_id": ObjectId(requestID)}, { "$set": { "finished": True } })

    flash("You have successfully completed this task", "success")
    return redirect(url_for("dashboard"))

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
        address = request.form.get("address")

        try:
            location = rq.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + str(address) + '&key=' + googleAPIKey).content
            location = json.loads(location)["results"][0]["geometry"]["location"]
            request_dicts= {
                "task": task,
                "user": session.get("user").get("id"),
                "volunteer": None,
                "category": category,
                "description": description,
                "dateRequested": datetime.now(),
                "finished": False,
                "address": address,
            }

            requests.insert_one(request_dicts)
            return redirect(url_for("dashboard"))
        except:
            flash(address + " is an invalid address.", "danger")
            return render_template("request.html", requestForm = requestForm)
        
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
        users.insert_one(new_user)
        return redirect(url_for("login"))
        # session["user"] = {"email": email, "first_name": first_name, "last_name": last_name, "id": new_user_id}
        flash("You have successfully signed up", "success")
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
            
            session["user"] = {"email": email, "first_name": user.get("first_name"), "last_name": user.get("last_name"),"id": str(user.get("_id"))}
            
            flash("You have successfully logged in", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Wrong email / password", "danger")
    
    return render_template("login.html", loginForm=loginForm)

@app.route('/logout')
def logout():
    session.pop("user")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.debug = True
    app.run()

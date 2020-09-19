import pymongo
import urllib.parse
from pymongo import MongoClient
from flask import Flask, render_template, flash, request, session, redirect, url_for
from datetime import datetime
import json

app = Flask(__name__)

# must run python3 -m pip install 'pymongo[srv]'
# documentation: https://pymongo.readthedocs.io/en/stable/tutorial.html
app.config['SECRET_KEY'] = "KIUYGY(H't76$A%U$6"
client = MongoClient(
    "mongodb+srv://admin:ibqamgEqZgrWoEJP@cluster0.j7aiy.mongodb.net/stoop?retryWrites=true&w=majority")
db = client.stoop
users = db.users
volunteers = db.volunteers
requests = db.requests


@app.route('/', methods=['POST', 'GET'])
def home():
    if not session.get("email"):
        return redirect(url_for('login'))
    # this is the send orders page
    return "Hello World"


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if session.get("email"):
        return "Send to home page"
    email = request.json['email']
    password = request.json['password']
    first_name = request.json['firstName']
    last_name = request.json['lastName']

    # check if user in database already
    if users.find_one({"email": email}):
        return  # return that user already exists

    new_user = {"email": email, "password": password,
                "first_name": first_name, "last_name": last_name}
    new_user_id = users.insert_one(new_user)
    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get("email"):
        return "Send to home page"
    email = request.json['email']
    password = request.json['password']

    # check if user in database
    user = users.find_one({"email": email})
    if password == user.password:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


if __name__ == "__main__":
    # print(users.find_one({"id": 0}))
    # print(volunteers.find_one({"id": 0}))
    # print(requests.find_one({"id": 0}))
    app.debug = True
    app.run()

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
        return "Send to login page"
    return "Hello World"


@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get("email"):
        return "Send to home page"
    # to do: get email + password from post args and pass them to database
    email = request.json['email']
    password = request.json['password']
    print(email)
    print(password)
    return "Login page"


if __name__ == "__main__":
    # print(users.find_one({"id": 0}))
    # print(volunteers.find_one({"id": 0}))
    # print(requests.find_one({"id": 0}))
    app.debug = True
    app.run()

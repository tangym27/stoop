import pymongo
import urllib.parse
from pymongo import MongoClient
from flask import Flask, render_template, flash, request, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# must run python3 -m pip install 'pymongo[srv]'
# documentation: https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient("mongodb+srv://admin:ibqamgEqZgrWoEJP@cluster0.j7aiy.mongodb.net/stoop?retryWrites=true&w=majority")
db = client.stoop
users = db.users
volunteers = db.volunteers
requests = db.requests

@app.route('/', methods=['POST', 'GET'])
def home():
    return "Hello World"

@app.route('/login', methods=['POST', 'GET'])
def home():
    return "Hello World" 

if __name__ == "__main__":
    # print(users.find_one({"id": 0}))
    # print(volunteers.find_one({"id": 0}))
    # print(requests.find_one({"id": 0}))
    app.debug=True
    app.run() 

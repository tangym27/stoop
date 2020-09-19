import flask
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects import postgresql
from application import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.Text)

    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)

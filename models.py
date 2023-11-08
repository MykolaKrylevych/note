from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
import os
import jwt
from werkzeug.security import generate_password_hash
from time import time


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    notes = relationship("Notes", back_populates="user")

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def get_reset_token(self, expires=500):
        return jwt.encode({'reset_password': self.email, 'exp': time() + expires},
                          key=os.getenv("FLASK_SECRET_KEY"))

    @staticmethod
    def verify_reset_token(token):
        try:
            email = jwt.decode(token, key=os.getenv("FLASK_SECRET_KEY"), algorithms=['HS256'])['reset_password']
        except Exception as e:
            return e
        return User.query.filter_by(email=email).first()

    def set_new_password(self, password):
        self.password = generate_password_hash(password)
        db.session.commit()


class Notes(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    notes_header = db.Column(db.String(1000))
    notes = db.Column(db.String(1000))
    border_color = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="notes")


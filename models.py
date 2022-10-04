"""SQLAlchemy models for Team Rater"""
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """Model for Team Rater User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.Text, nullable=False, unique=True)
    
    username = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    @classmethod
    def signup(cls, email, username, password):
        """Signs up a user and hashes password."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        new_user = User(email=email, username=username, password=hashed_pwd)

        db.session.add(new_user)
        return new_user

    @classmethod
    def authenticate(cls, username, password):
        """Authenticates a user with username and password."""

        user = cls.query.filter_by(username=username)
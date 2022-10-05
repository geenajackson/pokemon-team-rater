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

        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(email=email, username=username, password=hashed_pwd)

        db.session.add(new_user)
        return new_user

    @classmethod
    def authenticate(cls, username, password):
        """Authenticates a user with username and password."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        
        return False

class Team(db.Model):
    """Model referring to a team of Pokemon."""

    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))
    details = db.Column(db.Text)

class Pokemon(db.Model):
    """Information about a specific Pokemon."""

    __tablename__ = "pokemon"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    image = db.Column(db.Text, default="/static/images/poke-ball.png")
    type_1 = db.Column(db.Text, nullable=False)
    type_2 = db.Column(db.Text)

class Move(db.Model):
    """Information about a Pokemon Move."""

    __tablename__ = "moves"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    # moves with no power are null
    power = db.Column(db.Integer)
    # moves that always hit are null
    accuracy = db.Column(db.Integer)
    pp = db.Column(db.Integer)

class Moveset(db.Model):
    """Connection of a Pokemon <-> a move."""

    __tablename__ = "pokemon_moveset"

    id = db.Column(db.Integer, primary_key=True)
    poke_id = db.Column(db.Integer, db.ForeignKey("pokemon.id", ondelete="cascade"))
    move_id = db.Column(db.Integer, db.ForeignKey("moves.id", ondelete="cascade"))

class Team_Member(db.Model):
    """Connection of a team <-> a Pokemon."""

    __tablename__ = "team_members"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id", ondelete="cascade"))
    poke_id = db.Column(db.Integer, db.ForeignKey("pokemon.id", ondelete="cascade"))

class Comment(db.Model):
    """A comment on a team."""

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id", ondelete="cascade"))
    comment = db.Column(db.Text, nullable=False)
    commenter_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))

class Rating(db.Model):
    """A rating on a team."""

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id", ondelete="cascade"))
    rating = db.Column(db.Integer, nullable=False)
    rater_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)

import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from forms import LoginForm, CommentForm, UserSignUpForm
from models import db, connect_db, User

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///teamrater'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)
db.create_all()

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "super effective secret")
toolbar = DebugToolbarExtension(app)

##################################################################################
# User signup/login/logout routes

@app.before_request
def add_user_to_g():
    """Adds current user to Flask global if logged in."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Adds user to current session."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Removes user from current session."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handles user signup.

    Redirects to home when valid form submitted.

    If not valid form, present form.
    """

    form = UserSignUpForm()

##################################################################################
# Homepage and redirect to signup.

@app.route("/")
def homepage():
    """Shows homepage. Redirects user to signup if not logged in."""

    if g.user:
        return render_template("home.html")
    
    else:
        return redirect("/signup")
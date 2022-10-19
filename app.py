import os
import requests

from flask import Flask, Response, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from forms import UserSignUpForm, LoginForm, TeamForm, edit_team_form, CommentForm, edit_comment_form, RatingForm
from models import Rating, db, connect_db, User, Team, Pokemon, Comment

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
# User related routes

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

    if form.validate_on_submit():
        try:
            new_user = User.signup(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data
            )
            db.session.commit()
        except IntegrityError:
            flash("Username/Email already taken.", "danger")
            return render_template("/user/signup.html", form=form)
        
        do_login(new_user)
        flash("Created your account!", "success")

        return redirect("/")
    
    else:
        return render_template("/user/signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs in a user."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        
        if user:
            do_login(user)
            flash(f"Welcome, {user.username}!", "success")
            return redirect("/")
        
        flash("Invalid credentials.", "danger")
    
    return render_template("/user/login.html", form=form)

@app.route("/users/<int:user_id>")
def show_user_teams(user_id):
    """Shows teams for a specific user."""
    
    if not g.user:
        flash("Log in to view this page!", "warning")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    teams = (Team
            .query
            .filter(Team.user_id == user_id)
            .order_by(Team.id.desc())
            .all())

    return render_template("/user/show.html", user=user, teams=teams)

@app.route("/logout")
def logout():
    """Logs out a user."""
    do_logout()
    return redirect("/")
##################################################################################
# Homepage and redirect to signup.

@app.route("/")
def homepage():
    """Shows homepage if logged in. Renders signup/login choices if not."""

    if g.user:
        teams = (Team.query.order_by(Team.id.desc()).limit(100).all())
        return render_template("home.html", teams=teams)
    
    else:
        return render_template("home-anon.html")

##################################################################################
# Team CRUD routes.

@app.route("/teams/new", methods=["GET", "POST"])
def new_team():
    """Creates a new team of Pokemon."""

    if not g.user:
        flash("Log in to view this page!", "warning")
        return redirect("/")

    form = TeamForm()

    if form.validate_on_submit():
        team = Team(
            name = form.name.data,
            details = form.details.data,
            user_id = g.user.id
        )
        
        db.session.add(team)
        db.session.commit()
        flash("New team created!", "success")
        return redirect(f"/teams/{team.id}/show")
    
    return render_template("/team/new-team.html", form=form)


@app.route("/teams/<int:team_id>/search")
def search_pokemon(team_id):
    """Display a search bar for adding Pokemon to a team."""

    if not g.user:
        flash("Log in to view this page!", "warning")
        return redirect("/")

    team = Team.query.get_or_404(team_id)

    if team.user_id != g.user.id:
        flash("Access unauthorized.", "warning")
        return redirect("/")

    return render_template("/pokemon/search.html", team=team)



@app.route("/teams/<int:team_id>/add", methods=["POST"])
def add_pokemon(team_id):
    """Adds selected Pokemon to the team."""

    if not g.user:
        flash("Log in to view this page!", "warning")
        return redirect("/")

    team = Team.query.get_or_404(team_id)

    if team.user_id != g.user.id:
        flash("Access unauthorized.", "warning")
        return redirect("/")
    
    pokemon = request.form["pokemon"]

    add_pokemon = Pokemon.query.filter_by(name=pokemon).first()

    if add_pokemon:
        team.members.append(add_pokemon)
        db.session.commit()

        flash(f"Your new pokemon is: {add_pokemon.name}", "success")

        return redirect(f"/teams/{team.id}/show")


    else: 
        json_pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}").json()

        try:
            new_pokemon = Pokemon(
                name=json_pokemon["name"],
                image=json_pokemon["sprites"]["front_default"],
                type_1=json_pokemon["types"][0]["type"]["name"],
                type_2=json_pokemon["types"][1]["type"]["name"]
            )

        except IndexError:
            new_pokemon = Pokemon(
                name=json_pokemon["name"],
                image=json_pokemon["sprites"]["front_default"],
                type_1=json_pokemon["types"][0]["type"]["name"],
        )       



        db.session.add(new_pokemon)
        team.members.append(new_pokemon)
        db.session.commit()

        flash(f"Your new pokemon is: {new_pokemon.name}", "success")

        return redirect(f"/teams/{team.id}/show")

@app.route("/teams/<int:team_id>/remove", methods=["POST"])
def remove_pokemon(team_id):
    """Removes a pokemon from a team."""

    if not g.user:
        flash("Log in to view this page!", "warning")
        return redirect("/")

    team = Team.query.get_or_404(team_id)

    if team.user_id != g.user.id:
        flash("Access unauthorized.", "warning")
        return redirect("/")
    
    pokemon = int(request.form["pokemon"])

    removed_pokemon = team.members[pokemon]

    db.session.delete(removed_pokemon)
    db.session.commit()

    flash("Pokemon removed.", "warning")
    return redirect(f"/teams/{team_id}/edit")

@app.route("/teams/<int:team_id>/show", methods=["GET", "POST"])
def show_team(team_id):
    """Shows one team's details, comments, and ratings."""

    if not g.user:
        flash("Log in to view this page!", "warning")
        return redirect("/")
    
    team = Team.query.get_or_404(team_id)
    user = User.query.get(team.user_id)
    comments = Comment.query.filter_by(team_id=team_id).order_by(Comment.id)
    try:
        team_rating = round(
            Rating
            .query
            .with_entities(func.avg(Rating.rating).label("average"))
            .filter_by(team_id=team_id)
            .scalar(), 2)
    except:
        team_rating = "N/A"

    form = CommentForm()
    rating_form = RatingForm()

    if form.validate_on_submit():
        comment = Comment(
            team_id=team_id,
            comment=form.comment.data,
            commenter_id=g.user.id)

        db.session.add(comment)
        db.session.commit()


        flash("Comment added!", "success")
        return redirect(f"/teams/{team_id}/show")


    return render_template("/team/show.html", team=team, user=user, form=form, rating_form=rating_form, comments=comments, team_rating=team_rating)

    

@app.route("/teams/<int:team_id>/edit", methods=["GET", "POST"])
def edit_team(team_id):
    """Edits a team's details and Pokemon."""

    if not g.user:
        flash("Log in to view this page!", "warning")
        return redirect("/")

    team = Team.query.get_or_404(team_id)

    if team.user_id != g.user.id:
        flash("Access unauthorized.", "warning")
        return redirect("/")

    form = edit_team_form(team)
    

    if form.validate_on_submit():
        name = form.name.data
        details = form.details.data

        team.name = name
        team.details = details
        
        db.session.add(team)
        db.session.commit()

        flash("Team updated.", "success")

        return redirect(f"/teams/{team.id}/show")
    
    return render_template("/team/edit.html", form=form, team=team)

@app.route("/teams/<int:team_id>/delete", methods=["POST"])
def delete_team(team_id):
    """Deletes a team."""

    if not g.user:
        flash("Log in to view this page!", "warning")
        return redirect("/")

    team = Team.query.get_or_404(team_id)

    if team.user_id != g.user.id:
        flash("Access unauthorized.", "warning")
        return redirect("/")

    db.session.delete(team)
    db.session.commit()
    flash("Team deleted.", "danger")

    return redirect(f"/users/{g.user.id}")

##################################################################################
# Comment edit and delete routes

@app.route("/comments/<int:comment_id>/edit", methods=["GET", "POST"])
def edit_comment(comment_id):
    """Edits a comment."""

    if not g.user:
        flash("Log in to view this page!", "warning")
        return redirect("/")

    comment = Comment.query.get_or_404(comment_id)
    team = Team.query.get_or_404(comment.team_id)

    if comment.commenter_id != g.user.id:
        flash("Access unauthorized.", "warning")
        return redirect("/")
    
    form = edit_comment_form(comment)

    if form.validate_on_submit():
        new_comment = form.comment.data

        comment.comment = new_comment
        
        db.session.add(comment)
        db.session.commit()

        flash("Team updated.", "success")

        return redirect(f"/teams/{team.id}/show")
    
    return render_template("/team/comment-edit.html", form=form, comment=comment, team=team)

@app.route("/comments/<int:comment_id>/delete", methods=["POST"])
def delete_comment(comment_id):
    """Deletes a comment."""

    if not g.user:
        flash("Log in to view this page!", "warning")
        return redirect("/")

    comment = Comment.query.get_or_404(comment_id)
    team = Team.query.get_or_404(comment.team_id)

    if comment.commenter_id != g.user.id:
        flash("Access unauthorized.", "warning")
        return redirect("/")

    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted.", "danger")

    return redirect(f"/teams/{team.id}/show")

##################################################################################
# Rating routes

@app.route("/teams/<int:team_id>/show/rating/<int:rating>/submit", methods=["POST"])
def submit_rating(team_id, rating):

    if not g.user:
        flash("Log in to view this page!", "warning")
        return redirect("/")

    team = Team.query.get_or_404(team_id)

    if team.user_id == g.user.id:
        return "warning"
    
    search_rating = Rating.query.filter_by(team_id=team_id, rater_id=g.user.id).first()

    if search_rating:
        search_rating.rating = rating

        db.session.add(search_rating)
        db.session.commit()

        return "update"
    
    new_rating = Rating(team_id=team_id, rating=rating, rater_id=g.user.id)

    db.session.add(new_rating)
    db.session.commit()

    return "success"
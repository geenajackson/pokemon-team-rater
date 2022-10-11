from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class UserSignUpForm(FlaskForm):
    """Form for adding a new user."""

    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=8)])

class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=8)])

class TeamForm(FlaskForm):
    """Form for creating a new team."""

    name = StringField("Name of Team:", validators=[DataRequired(), Length(max=100)])
    details = TextAreaField("About your team:", default="N/A")

class CommentForm(FlaskForm):
    """Form for adding a comment."""

    comment = TextAreaField("Comment", validators=[DataRequired()])

def edit_team_form(team):
    """Function for editing a team"""
    class EditTeamForm(FlaskForm):
        """Form for editing a team."""
        name = StringField("Team Name", default=team.name, validators=[DataRequired(), Length(max=100)])
        details = TextAreaField("Details", default=team.details, validators=[DataRequired()])
    
    return EditTeamForm()

def edit_comment_form(com):
    """Function for editing a comment"""
    class EditCommentForm(FlaskForm):
        """Form for editing a comment"""
        comment = TextAreaField("Comment", default=com.comment, validators=[DataRequired()])
    
    return EditCommentForm()
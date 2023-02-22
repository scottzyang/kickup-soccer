from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.fields.html5 import DateField, TimeField
from kickup_app.extensions import bcrypt
from kickup_app.models import *

class UserForm(FlaskForm):
    '''Form to update user details'''
    username = StringField('Username', validators=[Length(min=3, max=80)])
    profile_picture = StringField('Profile Picture URL')
    first_name = StringField('First name', validators=[Length(max=80)])
    last_name = StringField('Last name', validators=[Length(max=80)])
    position = SelectField('Position', choices=Position.choices())

    submit = SubmitField('Submit')

class TeamForm(FlaskForm):
    '''Form to create new team'''
    team_name = StringField('Team Name', validators=[DataRequired(), Length(min=3, max=80)])
    logo_url = StringField('Team Image URL')

    submit = SubmitField('Submit')

    def validate_team(self, team_name):
        team = Team.query.filter_by(team_name=team_name.data).first()
        if team:
            raise ValidationError('That team name is taken. Please choose a different one.')

class GameForm(FlaskForm):
    '''Form to create new game'''
    name = StringField('Game Title', validators=[DataRequired(), Length(min=3, max=100)])
    location = StringField('Game Location', validators=[DataRequired(), Length(min=3, max=100)])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    home_team = QuerySelectField('Home Team', query_factory=lambda: Team.query)
    away_team = QuerySelectField('Away Team', query_factory=lambda: Team.query)

    submit = SubmitField('Submit')

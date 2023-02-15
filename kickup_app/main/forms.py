from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.fields.html5 import DateField
from kickup_app.extensions import bcrypt
from kickup_app.models import *

class TeamForm(FlaskForm):
    '''Form to create new team'''
    team_name = StringField('Team Name', validators=[DataRequired(), Length(min=3, max=80)])
    logo_url = StringField('Team Image URL')

    submit = SubmitField('Submit')

    def validate_team(self, team_name):
        team = Team.query.filter_by(team_name=team_name.data).first()
        if team:
            raise ValidationError('That username is taken. Please choose a different one.')

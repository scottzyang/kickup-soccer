from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.fields.html5 import DateField
from kickup_app.extensions import bcrypt
from kickup_app.models import *

class SignUpForm(FlaskForm):
    '''Form to create a new User'''
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80)])
    profile_picture = StringField('Profile Picture URL')
    first_name = StringField('First name', validators=[DataRequired(), Length(max=80)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(max=80)])
    birth_date = DateField('Birthday', validators=[DataRequired()])
    position = SelectField('Position', choices=Position.choices())

    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    
class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')

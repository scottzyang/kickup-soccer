# Create your models here.
from kickup_app.extensions import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)

class Position(FormEnum):
    ATTACKER = 'Attacker'
    DEFENDER = 'Defender'
    MIDFIELDER = 'Midfielder'
    GOALKEEPER = 'Goalkeeper'

class User(db.Model):
    """User Model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    birth_date = db.Column(db.Date)
    position = db.Column(db.Enum(Position), default=Position)

    # user linkage to team
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    team = db.relationship('Team', back_populates='players')

    def __str__(self):
        return f'Name: {self.first_name} {self.last_name}\nPosition: {self.position}'

    def __repr__(self):
        return f'Name: {self.first_name} {self.last_name}\nPosition: {self.position}'

class Team(db.Model):
    """Team Model"""
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(80), nullable=False)

    players = db.relationship('User', back_populates='team')
  
    def __str__(self):
        return f'Team Name: {self.team_name}'

    def __repr__(self):
        return f'Team Name: {self.team_name}'

# table to link player with teams
# user_team_table = db.Table('user_team', 
#     db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
# )

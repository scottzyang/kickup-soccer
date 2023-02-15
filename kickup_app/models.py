# Create your models here.
from kickup_app.extensions import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
from datetime import datetime
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

class User(UserMixin, db.Model):
    """User Model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profile_picture = db.Column(db.String(), nullable=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    birth_date = db.Column(db.Date)
    position = db.Column(db.Enum(Position))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

    # user linkage to team
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
    
class Game(db.Model):
    """Game Model"""
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(80), nullable=False)
    time = db.Column(db.Date)

    # link team to team ID
    home_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)
    away_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)

    # foreign key links, refers to the FK id's above and establishes relationship with the team.id
    home_team = db.relationship('Team', foreign_keys=[home_id])
    away_team = db.relationship('Team', foreign_keys=[away_id])

    def __str__(self):
        return f'Game time: {self.time}\nLocation: {self.location}'

    def __repr__(self):
        return f'Game time: {self.time}\nLocation: {self.location}'

# table to link game with teams

# Create your models here.
from kickup_app import db
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
    position = db.Column(db.Enum(Position, name="position_enum"))
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
    logo_url = db.Column(db.String(), nullable=True)
    date_formed = db.Column(db.Date)

    # relationship lists
    players = db.relationship('User', back_populates='team')
    home_games = db.relationship('Game', back_populates="home_team", foreign_keys="Game.home_id")
    away_games = db.relationship('Game', back_populates="away_team", foreign_keys="Game.away_id")
  
    def __str__(self):
        return f'{self.team_name}'

    def __repr__(self):
        return f'Team Name: {self.team_name}'
    
class Game(db.Model):
    """Game Model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    # link team to team ID
    home_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)
    away_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)

    # foreign key links, refers to the FK id's above and establishes relationship with the team.id
    home_team = db.relationship('Team', back_populates="home_games", foreign_keys=[home_id])
    away_team = db.relationship('Team', back_populates="away_games", foreign_keys=[away_id])

    def __str__(self):
        return f'Game time: {self.time}\nLocation: {self.location}'

    def __repr__(self):
        return f'Game time: {self.time}\nLocation: {self.location}'

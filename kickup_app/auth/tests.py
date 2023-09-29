# Create your tests here.
import os
from unittest import TestCase
import app

from datetime import datetime
from kickup_app.extensions import app, db, bcrypt
from kickup_app.models import *

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password,
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_user():
    team = Team(team_name="Firebenders", logo_url="https://picsum.photos/200/300", date_formed=datetime.now())
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user1 = User(username="scottyang", password=password_hash, profile_picture="https://picsum.photos/200/300", first_name="scott", last_name="yang", birth_date=datetime(1996, 8, 31), position=Position.ATTACKER)
    team.players.append(user1)
    db.session.add(user1)
    db.session.add(team)
    db.session.commit()

def create_team():
    team1 = Team(team_name="Airbenders", logo_url="https://picsum.photos/200/300", date_formed=datetime.now())
    db.session.add(team1)
    db.session.commit()

def create_game():
    team1 = Team(team_name="Waterbenders", logo_url="https://picsum.photos/200/300")
    team2 = Team(team_name="Firebenders", logo_url="https://picsum.photos/200/300")

    game = Game(name="Water vs Fire", location="Southern Water Tribe", date=datetime(2023, 3, 23), time=datetime.time(13, 30, 0, 0), home_id=1, away_id=1)

    db.session.add(game)
    db.session.add(team1)
    db.session.add(team2)
    db.session.commit()
    
class AuthTest(TestCase):
    '''Tests for authentication (login & sign up)'''

    def setUp(self):
        '''Run before each test'''
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):      
        create_user()  
        form_data = {
            'username': 'pusheen',
            'password': 'password',
            'profile_picture': "https://picsum.photos/200/300",
            "first_name": "scott", 
            "last_name": "yang",
            "birth_date": datetime(1996, 8, 31),   
            "position": Position.ATTACKER,
        }

        self.app.post('/signup', data=form_data)

        new_user = User.query.filter_by(username="pusheen").one()
        self.assertIsNone(new_user)
        self.assertEqual(new_user.username, 'pusheen')


    def test_signup_existing_user(self):

        create_user()

        form_data = {
            'username': 'scottyang',
            'password': 'password'
        }
        response = self.app.post('/signup', data=form_data)
        response_data = response.get_data(as_text=True)

        self.assertIn('That username is taken. Please choose a different one.', response_data)

    def test_login_correct_password(self):

        create_user()

        form_data = {
            'username': 'scottyang',
            'password': 'password'
        }

        response = self.app.post('/login', data=form_data)
        response_data = response.get_data(as_text=True)

        self.assertNotIn('Login', response_data)

    def test_login_nonexistent_user(self):
        form_data = {
            'username': 'scottzzzzzyang',
            'password': 'asdfasdf'
        }

        response = self.app.post('/login', data=form_data)
        response_data = response.get_data(as_text=True)

        self.assertIn('No user with that username. Please try again', response_data)
        
    def test_login_incorrect_password(self):
        create_user()

        form_data = {
            'username': 'scottyang',
            'password': 'pazzword'
        }
        response = self.app.post('/login', data=form_data)
        response_data = response.get_data(as_text=True)

        self.assertIn('Password doesn&#39;t match. Please try again.', response_data)

    def test_logout(self):
        create_user()
        
        form_data = {
            'username': 'scottyang',
            'password': 'password'
        }

        self.app.post('/login', data=form_data)
        response = self.app.get('/logout', follow_redirects=True)
        response_data = response.get_data(as_text=True)
  
        self.assertIn('Login', response_data)

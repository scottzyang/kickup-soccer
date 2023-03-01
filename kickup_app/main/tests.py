# Create your tests here.
import os
import unittest
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
    


class MainTests(unittest.TestCase):
    def setUp(self):
      '''Run after each test'''
      app.config['TESTING'] = True
      app.config['WTF_CSRF_ENABLED'] = False
      app.config['DEBUG'] = False
      app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
      self.app = app.test_client()
      db.drop_all()
      db.create_all()

    def test_homepage_logged_out(self):
        '''Test that homepage shows signup or login'''
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # check that these values are in the page
        response_text = response.get_data(as_text=True)
        self.assertIn('Sign Up', response_text)
        self.assertIn('Login', response_text)

        # check that these values are not in the page
        self.assertNotIn('View Players', response_text)
        self.assertNotIn('View Teams', response_text)
        self.assertNotIn('View Profile', response_text)

    def test_homepage_logged_in(self):
        '''Test that homepage shows additional options'''
        create_user()
        login(self.app, 'scottyang', 'password')

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('View Profile', response_text)
        self.assertIn('View Teams', response_text)
        self.assertIn('View Players', response_text)
        self.assertIn('View Games', response_text)
        self.assertIn('Create Team', response_text)
        self.assertIn('Setup a Game', response_text)

    def test_profile_logged_out(self):
        '''Test that profile endpoint redirects to login'''
        create_user()

        response = self.app.get('/profile/user1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Login Page', response_text)
        self.assertIn('<p class="text-white"><label for="username">Username:</label></p>', response_text)
        self.assertIn('KickUp Soccer', response_text)

    def test_profile_logged_in(self):
        '''Test that profile endpoint displays user data'''
        create_user()
        login(self.app, 'scottyang', 'password')

        response = self.app.get('/profile/scottyang', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('scottyang', response_text)
        self.assertIn('<p class="m-4 text-xl"><strong>Birthday: </strong>Aug, 31, 1996</p>', response_text)
        self.assertIn('<a class="font-serif border-solid border-8 border-white bg-white text-black hover:opacity-50 m-4 w-full" href="/profile/scottyang/settings">Settings</a>', response_text)
        self.assertIn('<p class="m-4 text-xl"><strong>Current Team: </strong>\n        \n          Firebenders\n        \n      </p>', response_text)

    def test_team_logged_out(self):
        '''Test that team profile redirects to login'''
        create_team()

        response = self.app.get('/team-details/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Login Page', response_text)
        self.assertIn('<p class="text-white"><label for="username">Username:</label></p>', response_text)
        self.assertIn('KickUp Soccer', response_text)

    def test_team_logged_in(self):
        '''Test that team profile redirects to login'''
        create_team()
        create_user()
        login(self.app, 'scottyang', 'password')

        response = self.app.get('/team-details/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Airbenders', response_text)
        self.assertIn('Upcoming Games:', response_text)
        self.assertIn('<a href="/profile/scottyang">Profile</a>', response_text)

    def test_update_profile(self):
        '''Test that profile update works'''
        create_user()
        login(self.app, 'scottyang', 'password')

        post_data = {
            'username': 'scottzyang',
            'profile_picture': "https://picsum.photos/200/300",
            'first_name': "Scotticus",
            'last_name': 'Yangicus'
        }

        self.app.post('/profile/scottyang/settings', data=post_data)
        profile = User.query.get(1)
        self.assertEqual(profile.username, 'scottyang')
        self.assertEqual(profile.first_name, 'scott')

    def test_delete_profile(self):
        '''Test that profile can be deleted and redirect'''
        create_user()
        login(self.app, 'scottyang', 'password')

        response = self.app.get('/delete-profile/scottyang', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Sign Up', response_text)
        self.assertIn('Login', response_text)
        self.assertIn('Game On!', response_text)

    def test_delete_team(self):
        '''Test that team can be deleted and redirect'''
        create_user()
        login(self.app, 'scottyang', 'password')

        response = self.app.get('/delete-team/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Registered Teams', response_text)

    def test_player_list(self):
        '''Test that player list displays players'''
        create_user()
        login(self.app, 'scottyang', 'password')

        response = self.app.get('/players', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('<p class="font-bold text-center text-lg mb-2">scott yang</p>', response_text)

    def test_teams_list(self):
        '''Test that teams list displays teams'''
        create_user()
        create_team()
        login(self.app, 'scottyang', 'password')

        response = self.app.get('/teams', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Airbenders', response_text)
        self.assertIn('Firebenders', response_text)




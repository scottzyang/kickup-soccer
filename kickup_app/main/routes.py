from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, time, date
from kickup_app.models import *
from kickup_app.main.forms import *

main = Blueprint('main', __name__)

# Create your routes here.
@main.route('/')
def homepage():
  test = "Homepage route should be working if you see this"

  return render_template('home.html', test=test)

@main.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
  user = User.query.filter_by(username=username).one()
  return render_template('user_profile.html', user=user)


@main.route('/create-team', methods=['GET', 'POST'])
@login_required
def create_team():
  form = TeamForm()
  if form.validate_on_submit():
    team = Team(
      team_name=form.team_name.data,
      logo_url=form.logo_url.data,
      date_formed=datetime.now()
    )
    db.session.add(team)
    db.session.commit()
    flash('Team Created.')
    return redirect(url_for('main.team_details', team_id=team.id))
  return render_template('create_team.html', form=form)

@main.route('/team-details/<team_id>', methods=['GET', 'POST'])
@login_required
def team_details(team_id):
  team = Team.query.get(team_id)
  return render_template('team_details.html', team=team)

@main.route('/create-game', methods=['GET', 'POST'])
@login_required
def create_game():
  form = GameForm()
  if form.validate_on_submit():
    game = Game(
      name=form.name.data,
      location=form.location.data,
      date=form.date.data,
      time=form.time.data,
      home_team=form.home_team.data,
      away_team=form.away_team.data,
    )
    db.session.add(game)
    db.session.commit()
    flash('Game successfully created. Game on!')
    return redirect(url_for('main.game_details', game_id=game.id)) 
  return render_template('create_game.html', form=form)

@main.route('/game-details/<game_id>', methods=['GET', 'POST'])
@login_required
def game_details(game_id):
  game = Game.query.get(game_id)
  return render_template('game_details.html', game=game)

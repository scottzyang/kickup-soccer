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

@main.route('/profile/<username>/settings', methods=['GET', 'POST'])
@login_required
def settings(username):
  user = User.query.filter_by(username=username).one()
  user_team = user.team
  user_form = UserForm()
  team_form = TeamForm()
  game_form = GameForm()

  if user_form.validate_on_submit():
    user.username = user.username if user_form.username.data == '' else user_form.username.data
    user.profile_picture = user.profile_picture if user_form.profile_picture.data == '' else user_form.profile_picture.data
    user.first_name = user.first_name if user_form.first_name.data == '' else user_form.first_name.data
    user.last_name = user.last_name if user_form.last_name.data == '' else user_form.last_name.data
    user.position = user.position if user_form.position.data =='' else user_form.position.data
    db.session.commit()
    flash('User Updated.')
    return redirect(url_for('main.profile', username=user_form.username.data))
  
  if team_form.validate_on_submit():
    user_team.team_name = user_team.team_name if team_form.team_name.data == '' else team_form.team_name.data
    user_team.logo_url = user_team.logo_url if team_form.logo_url.data == '' else team_form.logo_url.data
    db.session.commit()
    flash('Team Updated.')
    return redirect(url_for('main.team_details', team_id=user_team.id))
  return render_template('settings.html', user=user, user_form=user_form, team_form=team_form, game_form=game_form)

@main.route('/delete-profile/<username>', methods=["GET", "POST"])
@login_required
def delete_profile(username):
  user = User.query.filter_by(username=username).one()
  db.session.delete(user)
  db.session.commit()
  logout_user()
  return redirect(url_for('main.homepage'))

@main.route('/delete-team/<team_id>', methods=["GET", "POST"])
@login_required
def delete_team(team_id):
  team = Team.query.get(team_id)
  db.session.delete(team)
  db.session.commit()
  return redirect(url_for('main.teams_list'))

@main.route('/delete-game/<game_id>', methods=["GET", "POST"])
@login_required
def delete_game(game_id):
  game = Game.query.get(game_id)
  db.session.delete(game)
  db.session.commit()
  return redirect(url_for('main.games_list'))

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
  form = GameForm()

  if form.validate_on_submit():
    print('hello 2')
    game.name = game.name if form.name.data == '' else form.name.data
    game.location = game.location if form.location.data == '' else form.location.data
    game.date = game.date if form.date.data == '' else form.date.data
    game.time = game.time if form.time.data == '' else form.time.data
    game.home_team = game.home_team if form.home_team.data == '' else form.home_team.data
    game.away_team = game.away_team if form.away_team.data == '' else form.away_team.data
    db.session.commit()
    return redirect(url_for('main.game_details', game_id=game.id))
  else:
    print('form not validated')
  return render_template('game_details.html', game=game, form=form)

@main.route('/players', methods=['GET'])
@login_required
def players_list():
  players = User.query.all()
  return render_template('player_list.html', players=players)

@main.route('/teams', methods=['GET'])
@login_required
def teams_list():
  teams = Team.query.all()
  return render_template('teams_list.html', teams=teams)

@main.route('/games', methods=["GET"])
@login_required
def games_list():
  games = Game.query.all()
  return render_template('games_list.html', games=games)

@main.route('/join-team/<team_id>', methods=['GET', 'POST'])
@login_required
def join_team(team_id):
  user = User.query.filter_by(username=current_user.username).one()
  join_team = Team.query.filter_by(id=team_id).one()
  join_team.players.append(user)

  db.session.add(user)
  db.session.add(join_team)
  db.session.commit()
  return redirect(url_for('main.team_details', team_id=team_id))


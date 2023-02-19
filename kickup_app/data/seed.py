from kickup_app.models import * 
from kickup_app.extensions import bcrypt
from datetime import datetime
import csv

db.drop_all()
db.create_all()

# read csv file and return it
def read_csv(filename):
  rows = []
  with open(filename, 'r') as file:
      csvreader = csv.reader(file)
      header = next(csvreader)
      for row in csvreader:
          rows.append(row)
      return rows
  file.close()

# evaluate selection and convert to selection from Position Model
def position_selector(seed_position):
  position = None
  if seed_position == "Goalkeeper":
      position = Position.GOALKEEPER
  elif seed_position == "Defender":
      position = Position.DEFENDER
  elif seed_position == "Midfielder":
      position = Position.MIDFIELDER
  elif seed_position == "Attacker":
      position = Position.ATTACKER
  return position

def populate_data(data, model_type):
  if model_type == "User":
    for i in range(len(data)):
      hashed_password = bcrypt.generate_password_hash(data[0][1]).decode('utf-8')
      position = position_selector(data[i][6])
        

      new_user = User(
          username=data[i][0], 
          password=hashed_password, 
          profile_picture=data[i][2], 
          first_name=data[i][3],
          last_name=data[i][4],
          birth_date=datetime.strptime(data[i][5], "%Y-%m-%d"),
          position=position,
          team_id=data[i][7]
          )
      db.session.add(new_user)
      db.session.commit()
  elif model_type == "Team":
     for i in range(len(data)):
        new_team = Team(
           team_name=data[i][0],
           logo_url=data[0][1],
           date_formed=datetime.strptime(data[i][2], "%Y-%m-%d"),
        )
        db.session.add(new_team)
        db.session.commit()
  elif model_type == "Game":
     pass

# read csv file and populate database with users
user_data = read_csv('kickup_app/data/players.csv')
populate_data(user_data, "User")

# read csv file and populate database with teams
team_data = read_csv('kickup_app/data/teams.csv')
populate_data(team_data, "Team")

# read csv file and populate database with games
# game_data = read_csv('kickup_app/data/players.csv')
# populate_data(game_data, "Game")




from flask import Blueprint, render_template
from kickup_app.models import User, Team

main = Blueprint('main', __name__)

# Create your routes here.
@main.route('/')
def homepage():
  test = "Homepage route should be working if you see this"

  return render_template('home.html', test=test)


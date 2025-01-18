from flask import (
  Blueprint,
  render_template
)

view = Blueprint('view',__name__)

@view.route('/')
def root():
  return render_template('home.html', title="Update BOT"),200
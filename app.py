import random, string
from flask import Flask, render_template

TEAMS = [
  {
    'id': 1,
    'name': 'Tienervaders',
    'pin': 1356  
  },
  
  {
    'id': 2,
    'name': 'Harry en de hoempapas',
    'pin': 7619  
  },
  
  {
    'id': 3,
    'name': 'Pi-raten',
    'pin': 8853  
  },
  
  {
    'id': 4,
    'name': 'A.L. Bert en S. Tein',
    'pin': 4647  
  }
]

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)


@app.route('/')  # What happens when the user visits the site
def base_page():
	return render_template(
		'base.html',  # Template file path, starting from the templates folder. 
	)

@app.route('/stacking')
def stacking_base():
  return render_template(
    'stacking_base.html'
  )

@app.route('/stacking_submit')
def stacking_submit():
  return render_template(
    'stacking_submit.html',
    teams = TEAMS
  )
  
  
  
if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)
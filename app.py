import random, string
from flask import Flask, render_template, request

TEAMS = [
  {
    'id': '1',
    'name': 'Tienervaders',
    'pin': '1356'
  },
  
  {
    'id': '2',
    'name': 'Harry en de hoempapas',
    'pin': '7619'  
  },
  
  {
    'id': '3',
    'name': 'Pi-raten',
    'pin': '8853'  
  },
  
  {
    'id': '4',
    'name': 'A.L. Bert en S. Tein',
    'pin': '4647'  
  }
]

INSTANCES = [
  {
    'id': 0,
    'name': 'instance_voorbeeld.txt',
    'path': 'static/stacking_instances/instance_voorbeeld.txt'
  },
  
  {
    'id': 1,
    'name': 'instance_1.txt',
    'path': 'static/stacking_instances/instance_1.txt'
  },
  
  {
    'id': 2,
    'name': 'instance_2.txt',
    'path': 'static/stacking_instances/instance_2.txt' 
  },
  
  {
    'id': 3,
    'name': 'instance_3.txt',
    'path': 'static/stacking_instances/instance_3.txt' 
  },
]

def validate_pin(id: int=0, pin:int = 0) -> bool:
  for team in TEAMS:
    if team['id']==id and team['pin']==pin:
      return True
  return False

def check_stacking_submission(data) -> str:
  return "Succes! Score: 12"
  

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
    'stacking/base.html'
  )

@app.route('/stacking_submit')
def stacking_submit():
  return render_template(
    'stacking/submit.html',
    teams = TEAMS,
    instances = INSTANCES
  )


@app.route('/stacking_parse')
def parse_stacking():
  DATA = request.args
  valid_pin = validate_pin(id=DATA['id'], pin=DATA['pin'])
  if valid_pin:
    OUTPUT = check_stacking_submission(DATA)
    return render_template(
      '/stacking/parsed.html',
      data = DATA,
      output = OUTPUT
    )
  else:
    return render_template(
      'invalid_pin.html'
    )

@app.route('/stacking_instances')
def download_instances():
  return render_template(
    '/stacking/instances.html',
    instances=INSTANCES
  )

@app.route('/bier')
def beer_landing_page():
  return render_template(
    '/bier/base.html'
  )

@app.route('/planner')
def planner_landing_page():
  return render_template(
    '/planner/base.html'
  )

@app.route('/tripadvisor')
def tripadvisor_landing_page():
  return render_template(
    '/tripadvisor/base.html'
  )


if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)
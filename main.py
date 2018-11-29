#!flask/bin/python

# My Example to-do list application

# [START gae_python37_app]

# Flask bits
from flask import Flask, jsonify, abort, request, make_response, url_for

app = Flask(__name__)


# Helper function, create a full URI for a task
def make_public_task(task):
	new_task = {}
	
	for field in task:
		if field == 'id':
			new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
		else:
			new_task[field] = task[field]
	
	return new_task


# Some fake tasks, stored in-memory rather than in an external DB for now
tasks = [
			{"id":1,
			 "title": u"Buy video games",
			 "description": "I want Subnautica especially!",
			 "done": False},
			{"id":2,
			 "title": u"Learn Flask",
			 "description": "I don't know how this works but that won't stop me...",
			 "done":False}
		]
	
		
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
	return jsonify({'tasks': [make_public_task(task) for task in tasks]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
	
	# Filters list of results to tasks with matching id number
	task = [task for task in tasks if task['id'] == task_id]
	
	# If there's no results, abort and return "not found" HTTP response code
	if len(task) == 0:
		abort(404)
	
	# Weird quirk, line below will only return the first result in the
	# case that there are multiple matches...	
	return( jsonify({'task': task[0]}) )
	
	
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
	
	if not request.json or not 'title' in request.json:
		abort(400)
	
	task = {'id': tasks[-1]['id'] + 1,
			'title': request.json['title'],
			'description': request.json.get('description', ""),
			'done': False}
	
	tasks.append(task)
	return( jsonify({'task': task}), 201 )


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]
	
	if len(task) == 0:
		abort(404)
		
	if not request.json:
		abort(400)
	
	if 'title' in request.json and type(request.json['title']) is not unicode:
		abort(400)
		
	if 'description' in request.json and type(request.json['description']) is not unicode:
		abort(400)
			
	if 'done' in request.json and type(request.json['done']) is not bool:
		abort(400)
	
	task[0]['title'] = request.json.get('title', task[0]['title'])
	task[0]['description'] = request.json.get('description', task[0]['description'])
	task[0]['done'] = request.json.get('done', task[0]['done'])
	
	return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]
	if len(task) == 0:
		abort(404)
	tasks.remove(task[0])
	return jsonify({'result': True})
	

# This exists to replace default (human) HTML response in case of 404
# with a more machine-friendly json data dump that could be used by a
# GUI to trigger an appropriate report.
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)
	 	

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
    
# [END gae_python37_app]

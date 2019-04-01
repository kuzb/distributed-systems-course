import json
import time
from flask import Flask, jsonify
from celery import Celery
from celery.result import AsyncResult

app = Flask(__name__)
app.config.update( # These are not going to be used but needed as parameter
    CELERY_BROKER_URL='sqla+sqlite:///tasks_web.sqlite',
    CELERY_RESULT_BACKEND='db+sqlite:///results_web.db'
)

# Celery requires a solution to send and receive messages; 
# usually this comes in the form of a separate service called 
# a message broker.

# Celery, like a consumer appliance, doesn’t need much configuration to 
# operate. It has an input and an output. The input must be connected to 
# a broker, and the output can be optionally connected to a result backend. 

def make_celery(app):
	"""
	Require for Flask context, skip it
	"""
	c = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
	c.conf.update(app.config)
	TaskBase = c.Task

	class ContextTask(TaskBase):
		abstract = True
		def __call__(self, *args, **kwargs):
			with app.app_context():
				return TaskBase.__call__(self, *args, **kwargs)
	c.Task = ContextTask
	return c

celery = make_celery(app)

# task that is to be used in async call
@celery.task(name='server.todo') 
def insertion(todo): # task for adding todo
	with open('database.json', 'r') as db:
		items = json.loads(db.read())
	todos = [item['todo'] for item in items]
	if todo not in todos:
		items.append({'todo': todo})
		# imitating delay
		time.sleep(10) 
		with open('database.json', 'w') as db:
			db.write(json.dumps(items))
		return True

	return False

@app.route("/todo/<todo>") # Route for adding todos
def insert(todo):
	t = insertion.delay(todo) # Async call
	# "delay" method is used to call insertion task asyncronuesly with input todo
	return jsonify({
        	'msg': 'Your todo will be registered in a short time.',
        	'task': t.task_id # you an use it to track your task
    	})

@app.route("/status/<task>") # Route for checking the status of todo 
def status(task):
    res = celery.AsyncResult(task)
    
    return jsonify({
        	'status': res.ready()
    	})

if __name__ == '__main__':
	with open('database.json', 'w') as d:
		d.write(json.dumps([{'todo': 'exercise'},{'todo': 'drink'}]))
	app.run(debug=True)

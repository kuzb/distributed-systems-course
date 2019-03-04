from flask import  Flask, jsonify, request
from flask_restful import Resource, Api
import json
import random

app = Flask(__name__)
api = Api(app)

class number():
    def __init__(self, num = 1, start = 0, end = 1000000):
        self.num = num
        self.start = start
        self.end = end

    def setRandRange(self, start, end):
        self.start = start
        self.end = end

    def randomize(self):
        self.num = random.randint(self.start, self.end)

    def getNumber(self):
        return self.num

    def getRange(self):
        return self.start, self.end

rand = number()

# Standard routes
@app.route('/setRange/<int:start>/<int:end>')
def resettingRange(start,end):
    rand.setRandRange(start,end)
    return 'OK'

@app.route('/getRange')
def gettingRange():
    return json.dumps({
        'start' : str(rand.getRange()[0]),
        'end' : str(rand.getRange()[1])
    })

@app.route('/random')
def randomizeIt():
    rand.randomize()
    return 'OK'

# For rest
class guessNumber(Resource):
    def get(self, number):
        if number == rand.getNumber():
            return json.dumps({'result':'equal'})
        elif number > rand.getNumber():
            return json.dumps({'result':'less'})
        elif number < rand.getNumber():
            return json.dumps({'result':'more'})
    

# REST ROUTE(though not following the standard)
api.add_resource(guessNumber,'/guess/<int:number>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


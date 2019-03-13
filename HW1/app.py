from flask import  Flask, jsonify, request
from flask_restful import Resource, Api
import json
import random

app = Flask(__name__)
api = Api(app)

flights = []

class Flight(Resource):
    def get(self, id):
        for flight in flights:
            if(id == flight["id"]):
                return flight, 200
        return "User not found", 404
    
    def delete(self, id):
        global flights
        flights = [flight for flight in flights if flight["id"] != id]
        return "{} is deleted.".format(id), 200

api.add_resource(Flight, "/flight/<int:id>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import  Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import json
import random

app = Flask(__name__)
api = Api(app)

flight_id = 0
ticket_id = 0
flights = []

class Flight(Resource):
    def get(self, id):
        for flight in flights:
            if(int(id) == flight["id"]):
                return flight, 200
        return "User not found", 404
    
    def delete(self, id):
        for flight in flights:
            if(int(id) == flight["id"]):
                flights = [flight for flight in flights if flight["id"] != id]
                return "{} is deleted.".format(id), 200
        return "User not found", 404
        

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("dest")
        parser.add_argument("from")
        parser.add_argument("date")
        args = parser.parse_args()

        flight_id = flight_id + 1

        flight = {            
            "dest" : args["dest"],
            "from" : args["from"],
            "date" : args["date"],
            "id" : flight_id
        }

        flights.append(flight)
        return flight_id, 201
    
    def get(self):
        return flights, 200
            

api.add_resource(Flight, "/flights")
api.add_resource(Flight, "/flights/<int:id>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import  Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import random

app = Flask(__name__)
api = Api(app)

global flight_id
flight_id = 3
ticket_id = 0

class flight:
    def __init__(self):
        self.flights = []    

    def add(self, id, seats, dest, source, date):
        self.flights.append({
            "dest" : dest , 
            "from" : source , 
            "date" : date,
            "id" : id , 
            "seats" : seats ,
        })
        return {"flight_id": id }
    
    def incrementSeat(self, id):
        for flight in self.flights:
            if(id == flight["id"]):
                if flight["seats"] < 100:
                    flight["seats"] = flight["seats"] + 1
                    return 1
                else:
                    return 0, "No seat available"
        return 0, "Not Found"

    def delete(self, id):
        for flight in self.flights:
            if(id == flight["id"]):
                self.flights.remove(flight)
                return "{} is deleted.".format(id), 200
        return "User not found", 404

    def get(self, id):
        for flight in self.flights:
            if(id == flight["id"]):
                return flight, 200
        return "User not found", 404

    def getAll(self):
        print(self.flights)
        return self.flights

flights = flight()

flights.add(1, 12, "Istanbul", "Ankara","11-07-2019")
flights.add(2, 5, "Paris", "Hamburg","05-12-2019")
flights.add(3, 3, "London", "Moscow","19-03-2019")

class Flight(Resource):
    def get(self, id):
        return flights.get(int(id))
            
    def delete(self, id):
        return flights.delete(int(id))       
    
@app.route('/flights', methods=['GET'])
def getAllFlights():
    return jsonify(flights.getAll()), 200

@app.route('/flights', methods=['PUT'])
def addFlight():
    global flight_id 
    flight_id += 1
    print(flight_id)
    payload = request.json    
    return jsonify(flights.add(flight_id,0,payload["dest"],payload["from"],payload["date"])), 201

api.add_resource(Flight, "/flights/<int:id>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import  Flask, jsonify, request, Response
from flask_restful import Resource, Api, reqparse
import random

app = Flask(__name__)
api = Api(app)

global _FLIGHT_ID
global _PNR_ID

class seat:
    def __init__(self, flight_id):
        self.seatsAvaible = [0 for i in range(101)] # 0 meaning avaible
        self.numberOfSeatAvaible = 100
        self.flight_id = flight_id
    
    def reserveSeat(self):
        self.numberOfSeatAvaible -= 1

    def isFull(self):
        return self.numberOfSeatAvaible >= 0
    
    def isSeatEmpty(self, seatNumber):
        return self.seatsAvaible[seatNumber] == 0

    def chooseSeat(self, seatNumber, pnr):
        self.chooseSeat[seatNumber] = pnr

    def getSeatNumber(self, pnr):
        for seat in self.seatsAvaible:
            if seat == pnr:
                return seat
        return False

    def cancelReserveSeat(self):
        self.numberOfSeatAvaible += 1

    def cancelChooseSeat(self, seatNumber):
        self.chooseSeat[seatNumber] = 0

    def cancelChooseSeatByPNR(self, pnr):
        for seat in self.seatsAvaible:
            if seat == pnr:
                seat = 0
                return True
        return False

class flights:
    def __init__(self):
        self.all_flights = []    

    def add(self, id, dest, source, date):
        self.all_flights.append({
            "general" : {
                "dest" : dest , 
                "from" : source , 
                "date" : date,
                "flight_id" : id            
            },
            "seats" : seat(id)
            })
        return {"flight_id": id }
    
    def delete(self, id):
        for a_flight in self.all_flights:
            if(id == a_flight["general"]["flight_id"]):
                self.all_flights.remove(a_flight)
                return True
        return False

    def get(self, id):
        for a_flight in self.all_flights:
            if(id == a_flight["general"]["flight_id"]):
                return a_flight["general"]
    
    def isExist(self, id):
        for a_flight in self.all_flights:
            if(id == a_flight["general"]["flight_id"]):
                return True
        return False

    def getAll(self):
        temp = []
        for a_flight in self.all_flights:
            temp.append(a_flight["general"])
        return temp

    def getSeatObject(self, id):
        for a_flight in self.all_flights:
            if(id == a_flight["general"]["flight_id"]):
                return a_flight["seats"]

  

the_flights = flights()

the_flights.add(1, 12, "Istanbul", "Ankara","11-07-2019")
the_flights.add(2, 5, "Paris", "Hamburg","05-12-2019")
the_flights.add(3, 3, "London", "Moscow","19-03-2019")

# last used id
_FLIGHT_ID= 3

_PNR_ID = 0

class ticket:
    def __init__(self):
        self.all_tickets = []

    def add(self, flight_id, pnr_id):            
        self.all_tickets.append({
        "PNR" : pnr_id,
        "flight_id" : flight_id
        })

    def get(self, pnr):
        for a_ticket in self.all_tickets:
            if int(pnr) == a_ticket["PNR"]:
                return a_ticket
        return False

    def delete(self, pnr):
        for a_ticket in self.all_tickets:
            if int(pnr) == a_ticket["PNR"]:
                self.all_tickets.remove(a_ticket)
                return True
        return False

    def isExist(self, pnr):
        for a_ticket in self.all_tickets:
            if int(pnr) == a_ticket["PNR"]:
                return True
        return False

the_tickets = ticket()

class Ticket(Resource):
    def put(self): # buying a ticket for a given flight
        global _PNR_ID
        _PNR_ID += 1
        parser = reqparse.RequestParser()
        parser.add_argument("flight_id")
        args = parser.parse_args()
        if the_flights.isExist(int(args["flight_id"])):
            if the_flights.getSeatObject(int(args["flight_id"])).isFull():
                the_flights.getSeatObject(int(args["flight_id"])).reserveSeat()
                the_tickets.add(int(args["flight_id"]), _PNR_ID)
                return {
                    "PNR" : _PNR_ID
                }, 200
            return 409
        return 404

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("PNR")
        args = parser.parse_args()
        if args["PNR"]:
            if the_tickets.isExist(int(args["PNR"])):
                ticket = the_tickets.get(int(args["PNR"]))
                flight_id = ticket["flight_id"]
                flight = the_flights.get(flight_id)
                seat = the_flights.getSeatObject(flight_id)
                return {
                    "dest" : flight["dest"], 
                    "from" : flight["from"],
                    "date" : flight["date"],
                    "flight_id" : flight_id,
                    "seat_number" : seat.getSeatNumber(int(args["PNR"]))
                }, 200
            return 404
        # GetAll
        

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("PNR")
        parser.add_argument("seat_number")
        args = parser.parse_args()        
        if the_tickets.isExist(int(args["PNR"])):    
            flight_id = the_tickets.get("PNR")["flight_id"]   
            seat_obj =the_flights.getSeatObject(flight_id) 
            if seat_obj.isSeatEmpty(args["seat_number"]):
                return 200
            return 409
        return 404
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("PNR")
        args = parser.parse_args()        
        if the_tickets.isExist(int(args["PNR"])):  
            flight_id = the_tickets.get(int(args["PNR"]))["flight_id"]  
            the_tickets.delete(int(args["PNR"]))
            seat_obj = the_flights.getSeatObject(flight_id)
            seat_obj.cancelChooseSeatByPNR(int(args["PNR"]))
            seat_obj.cancelReserveSeat()
            return 200
        return 404     

# RESTFUL
class Flight(Resource):
    def get(self, id):
        if the_flights.isExist(int(id)):
            return  the_flights.get(int(id)), 200
        else:
            return 404 # Not Found
     
            
    def delete(self, id):
        if the_flights.delete(int(id)):
            return 200 # Deleted 
        else:
            return 404 # Not Found
     
    
@app.route('/flights', methods=['GET'])
def getAllFlights():
    return jsonify(the_flights.getAll()), 200

@app.route('/flights', methods=['PUT'])
def addFlight():
    global _FLIGHT_ID
    _FLIGHT_ID+= 1
    payload = request.json    
    return jsonify(the_flights.add(_FLIGHT_ID,0,payload["dest"],payload["from"],payload["date"])), 201

api.add_resource(Flight, "/flights/<int:id>")
api.add_resource(Ticket, "/tickets")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
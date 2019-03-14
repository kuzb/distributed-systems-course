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

    def cancelReserveSeat(self):
        self.numberOfSeatAvaible += 1

    def cancelChooseSeat(self, seatNumber):
        self.chooseSeat[seatNumber] = 0

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


    # didn't book the seat(position) yet
    # returns: boolFlightExists, boolSeatAvailable

    def registerTicket(self, id): 
        for a_flight in self.all_flights:
            if(id == a_flight["flight_id"]):
                if a_flight["seats"] < 100:
                    a_flight["seats"] = a_flight["seats"] + 1
                    return True, True # Flight exits and there is space
                return True, False # Flight exists but no space
        return False, False # Flight doesn't exists, all false

    def reserveSeat(self, id, seatNumber):
        for a_flight in self.all_flights:
            if(id == a_flight["flight_id"]):
                if a_flight["seat_available"][seatNumber]:
                    # Seat is reserved
                    a_flight["seat_available"][seatNumber] = False
                    return True
                return False # Seat is not available
        return False  # Flight doesn't exists

    def cancelSeat(self, id, seatNumber):
        for a_flight in self.all_flights:
            if(id == a_flight["flight_id"]):
                if not (a_flight["seat_available"][seatNumber]):
                    a_flight["seat_available"][seatNumber] = True
                    return True # Seat is again available
                return False # Seat was already available
        return False  # Flight doesn't exists
    
    def cancelTicket(self, id):
        for a_flight in self.all_flights:
            if(id == a_flight["flight_id"]):
                a_flight["seats"] = a_flight["seats"] - 1
                return True # Flight exits and one more seat available
        return False # Flight doesn't exists 

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
        for ticket in self.all_tickets:
            if int(pnr) == ticket["PNR"]:
                return ticket
        return jsonify({"PNR" : pnr}) ,404

    def chooseSeat(self,pnr, seat_id):
        for ticket in self.all_tickets:
            if int(pnr) == ticket["PNR"]:
                if the_flights.reserveSeat(ticket["flight_id"],seat_id-1):
                    ticket["seat_number"] = seat_id
                    return jsonify({
                        "PNR" : ticket["PNR"],
                        "seat_number" : seat_id
                    }), 200 # seat number is available
                return 409 # seat number is not available
        return 404 # PNR does not exist
    
    def getAll(self):
        temp = []
        for ticket in self.all_tickets:
            temp.append({
                "dest" : the_flights.get(ticket["flight_id"])["dest"],
                "from" : the_flights.get(ticket["flight_id"])["from"],
                "date" : the_flights.get(ticket["flight_id"])["date"],
                "flight_id" : ticket["flight_id"],
                "PNR" : ticket["PNR"]
            })
        return jsonify(temp), 200

    def delete(self, pnr):
        for ticket in self.all_tickets:
            if int(pnr) == ticket["PNR"]:
                the_flights.cancelSeat(ticket["flight_id"], ticket["seat_number"] - 1)
                the_flights.cancelTicket(ticket["flight_id"])
                self.all_tickets.remove(ticket)
                return jsonify({"PNR" : pnr}), 200
        return jsonify({"PNR" : pnr}), 400

the_tickets = ticket()

class Ticket(Resource):
    def put(self):
        global _PNR_ID
        _PNR_ID += 1
        parser = reqparse.RequestParser()
        parser.add_argument("flight_id")
        args = parser.parse_args()
        return Response(the_tickets.add(int(args["flight_id"])))

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("PNR")
        args = parser.parse_args()
        if args["PNR"]:
            return the_tickets.get(int(args["PNR"]))
        return Response(the_tickets.getAll())
        

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("PNR")
        parser.add_argument("seat_number")
        args = parser.parse_args()        
        return Response(the_tickets.chooseSeat(int(args["PNR"]),int(args["seat_number"])))
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("PNR")
        args = parser.parse_args()        
        return Response(the_tickets.delete(int(args["PNR"])))


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
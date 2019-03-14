from flask import  Flask, jsonify, request, Response
from flask_restful import Resource, Api, reqparse
import random

app = Flask(__name__)
api = Api(app)

global flight_id
global pnr_id

class seat:
    def __init__(self, flightid):
        self.seatsAvaible = [True for i in range(101)]
        self.numberOfSeatAvaible = 100
        self.flightID = flightid
    
    def reserveSeat(self):
        self.numberOfSeatAvaible -= 1
    
    def isSeatEmpty(self, seatNumber):
        return self.seatsAvaible[seatNumber]

    def chooseSeat(self, seatNumber):
        self.chooseSeat[seatNumber] = False

    



class flight:
    def __init__(self):
        self.flights = []    

    def add(self, id, dest, source, date):
        self.flights.append({
            "general" : {
                "dest" : dest , 
                "from" : source , 
                "date" : date,
                "flight_id" : id            
            },
            "seats" : seat()
            })
        return {"flight_id": id }
    
    def delete(self, id):
        for flight in self.flights:
            if(id == flight["general"]["flight_id"]):
                self.flights.remove(flight)
                return True
        return False

    def get(self, id):
        for flight in self.flights:
            if(id == flight["general"]["flight_id"]):
                return flight["general"]
    
    def isExist(self, id):
        for flight in self.flights:
            if(id == flight["general"]["flight_id"]):
                return True
        return False

    def getAll(self):
        temp = []
        for flight in self.flights:
            temp.append(flight["general"])
        return temp

    # didn't book the seat(position) yet
    # returns: boolFlightExists, boolSeatAvailable
    def registerTicket(self, id): 
        for flight in self.flights:
            if(id == flight["flight_id"]):
                if flight["seats"] < 100:
                    flight["seats"] = flight["seats"] + 1
                    return True, True # Flight exits and there is space
                return True, False # Flight exists but no space
        return False, False # Flight doesn't exists, all false

    def reserveSeat(self, id, seatNumber):
        for flight in self.flights:
            if(id == flight["flight_id"]):
                if flight["seat_available"][seatNumber]:
                    # Seat is reserved
                    flight["seat_available"][seatNumber] = False
                    return True
                return False # Seat is not available
        return False  # Flight doesn't exists

    def cancelSeat(self, id, seatNumber):
        for flight in self.flights:
            if(id == flight["flight_id"]):
                if not (flight["seat_available"][seatNumber]):
                    flight["seat_available"][seatNumber] = True
                    return True # Seat is again available
                return False # Seat was already available
        return False  # Flight doesn't exists
    
    def cancelTicket(self, id):
        for flight in self.flights:
            if(id == flight["flight_id"]):
                flight["seats"] = flight["seats"] - 1
                return True # Flight exits and one more seat available
        return False # Flight doesn't exists 

flights = flight()

flights.add(1, 12, "Istanbul", "Ankara","11-07-2019")
flights.add(2, 5, "Paris", "Hamburg","05-12-2019")
flights.add(3, 3, "London", "Moscow","19-03-2019")

# last used id
flight_id = 3

pnr_id = 0

class ticket:
    def __init__(self):
        self.tickets = []

    def add(self, flightID):
        exists, seat_available = flights.registerTicket(flightID)
        if seat_available:
            print("mother fucker")
            global pnr_id
            pnr_id += 1
            self.tickets.append({
            "PNR" : pnr_id,
            "flight_id" : flightID,
            "seat_number" : 0
            })
            return jsonify({"PNR" : pnr_id}) , 200
        elif exists:
            return jsonify({"PNR" : pnr_id}) , 409
        else:
            return jsonify({"PNR" : pnr_id}) , 404     

    def get(self, pnr):
        for ticket in self.tickets:
            if int(pnr) == ticket["PNR"]:
                return jsonify({
                    "dest" : flights.get(ticket["flight_id"])["dest"],
                    "from" : flights.get(ticket["flight_id"])["from"],
                    "date" : flights.get(ticket["flight_id"])["date"],
                    "flight_id" :ticket["flight_id"],
                    "seat_number" :ticket["seat_number"]
                }), 200
        return jsonify({"PNR" : pnr}) ,404

    def chooseSeat(self,pnr, seat_id):
        for ticket in self.tickets:
            if int(pnr) == ticket["PNR"]:
                if flights.reserveSeat(ticket["flight_id"],seat_id-1):
                    ticket["seat_number"] = seat_id
                    return jsonify({
                        "PNR" : ticket["PNR"],
                        "seat_number" : seat_id
                    }), 200 # seat number is available
                return 409 # seat number is not available
        return 404 # PNR does not exist
    
    def getAll(self):
        temp = []
        for ticket in self.tickets:
            temp.append({
                "dest" : flights.get(ticket["flight_id"])["dest"],
                "from" : flights.get(ticket["flight_id"])["from"],
                "date" : flights.get(ticket["flight_id"])["date"],
                "flight id" : ticket["flight_id"],
                "PNR" : ticket["PNR"]
            })
        return jsonify(temp), 200

    def delete(self, pnr):
        for ticket in self.tickets:
            if int(pnr) == ticket["PNR"]:
                flights.cancelSeat(ticket["flight_id"], ticket["seat_number"] - 1)
                flights.cancelTicket(ticket["flight_id"])
                self.tickets.remove(ticket)
                return jsonify({"PNR" : pnr}), 200
        return jsonify({"PNR" : pnr}), 400

tickets = ticket()

class Ticket(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("flight_id")
        args = parser.parse_args()
        return Response(tickets.add(int(args["flight_id"])))

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("PNR")
        args = parser.parse_args()
        if args["PNR"]:
            return tickets.get(int(args["PNR"]))
        return Response(tickets.getAll())
        

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("PNR")
        parser.add_argument("seat_number")
        args = parser.parse_args()        
        return Response(tickets.chooseSeat(int(args["PNR"]),int(args["seat_number"])))
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("PNR")
        args = parser.parse_args()        
        return Response(tickets.delete(int(args["PNR"])))


# RESTFUL
class Flight(Resource):
    def get(self, id):
        if flights.isExist(int(id)):
            return  flights.get(int(id)), 200
        else:
            return 404 # Not Found
     
            
    def delete(self, id):
        if flights.delete(int(id)):
            return 200 # Deleted 
        else:
            return 404 # Not Found
     
    
@app.route('/flights', methods=['GET'])
def getAllFlights():
    return jsonify(flights.getAll()), 200

@app.route('/flights', methods=['PUT'])
def addFlight():
    global flight_id 
    flight_id += 1
    payload = request.json    
    return jsonify(flights.add(flight_id,0,payload["dest"],payload["from"],payload["date"])), 201

api.add_resource(Flight, "/flights/<int:id>")
api.add_resource(Ticket, "/tickets")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
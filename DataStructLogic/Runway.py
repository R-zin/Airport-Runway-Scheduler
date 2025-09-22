# BackEnd/DataStructLogic/Runway.py

class Runway:
    def __init__(self, runway_id):
        self.runway_id = runway_id
        self.available = True
        self.current_flight = None

    def assign_flight(self, flight):
        if self.available:
            self.current_flight = flight
            self.available = False
            print(f"Runway {self.runway_id} assigned to Flight {flight.flight_number}")
        else:
            print(f"Runway {self.runway_id} is currently occupied.")

    def release_runway(self):
        if not self.available:
            print(f"Runway {self.runway_id} released from Flight {self.current_flight.flight_number}")
            self.current_flight = None
            self.available = True

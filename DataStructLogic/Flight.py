# BackEnd/DataStructLogic/Airport.py

from .Runway import Runway
from .Scheduling import add_flight, schedule_flights
from .DataModel import Flight

class Flight:
    def __init__(self, name, num_runways=2):
        self.name = name
        self.runways = [Runway(i+1) for i in range(num_runways)]

    def add_flight(self, flight):
        add_flight(flight)

    def schedule(self):
        print(f"\n--- Scheduling at {self.name} ---")
        schedule_flights()

    def assign_runway(self, flight):
        for runway in self.runways:
            if runway.available:
                runway.assign_flight(flight)
                return
        print("⚠️ No runways available, flight must wait!")

    def release_runway(self, runway_id):
        if 1 <= runway_id <= len(self.runways):
            self.runways[runway_id-1].release_runway()

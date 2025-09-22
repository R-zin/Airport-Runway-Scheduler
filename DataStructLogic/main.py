# BackEnd/DataStructLogic/main.py

from DataModel import Flight
from Airport import Airport

def main():
    airport = Airport("JFK", num_runways=2)

    # Sample Flights
    f1 = Flight("AI101", "New York", 5000, 2000, "Passenger", False, "Normal")
    f2 = Flight("AI102", "London", 3500, 500, "Cargo", True, "Emergency")
    f3 = Flight("AI103", "Paris", 2000, 800, "Passenger", False, "Normal")

    # Add flights to airport
    airport.add_flight(f1)
    airport.add_flight(f2)
    airport.add_flight(f3)

    # Schedule and assign runways
    airport.schedule()

if __name__ == "__main__":
    main()

# BackEnd/DataStructLogic/Scheduling.py

from queue import PriorityQueue
from .DataModel import Flight

# Global priority queue
pq = PriorityQueue()

def add_flight(flight: Flight):
    """
    Adds a Flight object to the priority queue based on its priority.
    """
    pq.put((flight.priority(), flight))
    print(f"[+] Flight {flight.flight_number} added with priority {flight.priority()}")

def schedule_flights():
    """
    Processes all flights in priority order.
    """
    print("\n--- Scheduling Flights ---")
    while not pq.empty():
        priority, flight = pq.get()
        print(f"[✓] Scheduling {flight}")

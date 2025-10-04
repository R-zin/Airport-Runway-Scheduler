"""
AirportManagementSystem.py
Main system that manages all airport operations.
"""

import heapq
from datetime import datetime
from Flight import Flight
from Runway import Runway
from AirportGraph import AirportGraph


class AirportManagementSystem:
    """Main system that manages all airport operations."""
    
    def __init__(self):
        self.flight_queue = []  # Priority queue for flight scheduling
        self.runway_queue = []  # Priority queue for runway allocation
        self.runways = [Runway(i+1) for i in range(3)]  # 3 runways
        self.cancellation_stack = []  # Stack for canceled flights
        self.airport_graph = AirportGraph()
        self.scheduled_flights = []  # List of currently scheduled flights
        
        # Add some sample routes
        self._add_sample_routes()
    
    def _add_sample_routes(self):
        """Add some sample airport routes."""
        routes = [
            ("JFK", "LAX", 5),
            ("JFK", "LHR", 7),
            ("LAX", "SFO", 1),
            ("LHR", "CDG", 1),
            ("SFO", "NRT", 10),
            ("CDG", "FRA", 1)
        ]
        for source, dest, distance in routes:
            self.airport_graph.add_route(source, dest, distance)
    
    def add_flight(self, flight_number, destination, departure_time_str, is_emergency=False):
        """Add a new flight to the system."""
        try:
            departure_time = datetime.strptime(departure_time_str, "%H:%M")
            flight = Flight(flight_number, destination, departure_time, is_emergency)
            heapq.heappush(self.flight_queue, flight)
            print(f"✓ Flight {flight} added to system")
            
            # Automatically add route if it doesn't exist
            if destination not in self.airport_graph.graph:
                self.airport_graph.add_route("JFK", destination, 5)  # Default distance
                
        except ValueError:
            print("❌ Invalid time format. Please use HH:MM (e.g., 14:30)")
    
    def schedule_flights(self):
        """Schedule flights based on priority and departure time."""
        if not self.flight_queue:
            print("No flights to schedule.")
            return
        
        print("\n--- Flight Scheduling ---")
        scheduled_count = 0
        
        while self.flight_queue:
            flight = heapq.heappop(self.flight_queue)
            self.scheduled_flights.append(flight)
            scheduled_count += 1
            print(f"✓ Scheduled: {flight}")
        
        print(f"\nTotal flights scheduled: {scheduled_count}")
    
    def allocate_runway(self):
        """Allocate available runways to waiting flights."""
        if not self.scheduled_flights:
            print("No scheduled flights to allocate runways to.")
            return
        
        print("\n--- Runway Allocation ---")
        allocated_count = 0
        
        for flight in self.scheduled_flights[:]:
            for runway in self.runways:
                if runway.is_available and runway.assign_flight(flight):
                    print(f"✓ {flight.flight_number} assigned to {runway}")
                    self.scheduled_flights.remove(flight)
                    allocated_count += 1
                    break
            else:
                print(f"⚠️ No runway available for {flight.flight_number}")
        
        print(f"\nRunways allocated: {allocated_count}")
        self._display_runway_status()
    
    def _display_runway_status(self):
        """Display current runway status."""
        print("\n--- Runway Status ---")
        for runway in self.runways:
            print(f"  {runway}")
    
    def find_route(self, start, destination):
        """Find shortest route between two airports."""
        print(f"\n--- Finding Route: {start} → {destination} ---")
        path, distance = self.airport_graph.find_shortest_route(start, destination)
        
        if path:
            print(f"✓ Route found: {' → '.join(path)}")
            print(f"Total distance: {distance}")
        else:
            print("❌ No connection available")
    
    def cancel_flight(self, flight_number):
        """Cancel a flight and add it to the cancellation log."""
        # Find flight in scheduled flights
        flight_to_cancel = None
        for flight in self.scheduled_flights:
            if flight.flight_number == flight_number:
                flight_to_cancel = flight
                break
        
        if flight_to_cancel:
            self.scheduled_flights.remove(flight_to_cancel)
            self.cancellation_stack.append(flight_to_cancel)
            print(f"✓ Flight {flight_number} canceled and added to cancellation log")
        else:
            # Also check if flight is currently assigned to a runway
            for runway in self.runways:
                if not runway.is_available and runway.current_flight.flight_number == flight_number:
                    flight_to_cancel = runway.release_runway()
                    self.cancellation_stack.append(flight_to_cancel)
                    print(f"✓ Flight {flight_number} canceled from runway and added to cancellation log")
                    return
            
            print(f"❌ Flight {flight_number} not found in scheduled flights or runways")
    
    def undo_last_cancellation(self):
        """Undo the last flight cancellation."""
        if self.cancellation_stack:
            canceled_flight = self.cancellation_stack.pop()
            self.scheduled_flights.append(canceled_flight)
            print(f"✓ Undid cancellation: {canceled_flight}")
        else:
            print("❌ No cancellations to undo")
    
    def display_status(self):
        """Display current system status."""
        print("\n--- System Status ---")
        print(f"Scheduled flights: {len(self.scheduled_flights)}")
        print(f"Canceled flights: {len(self.cancellation_stack)}")
        print(f"Available runways: {sum(1 for r in self.runways if r.is_available)}")
        
        if self.scheduled_flights:
            print("\nScheduled flights:")
            for flight in self.scheduled_flights:
                print(f"  - {flight}")
        
        if self.cancellation_stack:
            print("\nRecently canceled flights:")
            for flight in self.cancellation_stack[-3:]:  # Show last 3
                print(f"  - {flight}")

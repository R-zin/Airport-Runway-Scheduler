import heapq
from datetime import datetime
from Flight import Flight
from Runway import Runway
from AirportGraph import AirportGraph


class Managmement_System:
    """Manages flights, runways, cancellations, and routes."""

    def __init__(self):
        self.flight_queue = []          # Flights waiting to be scheduled
        self.scheduled_flights = []     # Flights already scheduled
        self.runways = [Runway(i+1) for i in range(3)]  # 3 runways
        self.canceled_flights = []      # Stack of canceled flights
        self.airport_graph = AirportGraph()
        self._add_sample_routes()
        self.history = []

    # ---------------- ROUTES ----------------
    def _add_sample_routes(self):
        routes = [
            ("JFK", "LAX", 5),
            ("JFK", "LHR", 7),
            ("LAX", "SFO", 1),
            ("LHR", "CDG", 1),
            ("SFO", "NRT", 10),
            ("CDG", "FRA", 1)
        ]
        for src, dst, dist in routes:
            self.airport_graph.add_route(src, dst, dist)
    def add_route(self,src,dest,distance):
        self.airport_graph.add_route(src,dest,distance)

    def find_route(self, start, destination):
        """Find and show the shortest route between two airports."""
        path, dist = self.airport_graph.find_shortest_route(start, destination)
        if path:
            print(f"Route: {' → '.join(path)} (Distance: {dist})")
        else:
            print("No route found.")

    # ---------------- FLIGHTS ----------------
    def add_flight(self, number, destination, time_str, emergency=False):
        """Add a flight to the system."""
        try:
            departure_time = datetime.strptime(time_str, "%H:%M")
            flight = Flight(number, destination, departure_time, emergency)
            flight.status = 'Added and awaiting scheduling'
            self.history.append(flight)
            heapq.heappush(self.flight_queue, flight)
            print(f"Added: {flight}")

            # If destination not in routes, add default route
            if destination not in self.airport_graph.graph:
                self.airport_graph.add_route("JFK", destination, 5)
        except ValueError:
            print("Invalid time format! Use HH:MM")

    def schedule_flights(self):
        """Move flights from queue to scheduled list."""
        if not self.flight_queue:
            print("No flights to schedule.")
            return
        while self.flight_queue:
            self.scheduled_flights.append(heapq.heappop(self.flight_queue))
        print(f"Scheduled {len(self.scheduled_flights)} flights.")

    # ---------------- RUNWAYS ----------------
    def allocate_runways(self):
        """Assign available runways to scheduled flights."""
        if not self.scheduled_flights:
            print("No flights waiting for runways.")
            return

        for flight in self.scheduled_flights[:]:
            for runway in self.runways:
                if runway.is_available and runway.assign_flight(flight):
                    flight.status = 'Runway Assigned'
                    flight.assigned_runway = runway
                    flight.assigned_runway_no = runway.runway_id
                    print(f"{flight.flight_number} → {runway}")
                    self.scheduled_flights.remove(flight)
                    break
        self._show_runways()

    def _show_runways(self):
        print("\nRunway Status:")
        for r in self.runways:
            print(" ", r)

    # ---------------- CANCELLATIONS ----------------
    def cancel_flight(self, number):
        """Cancel a scheduled or assigned flight."""
        # In scheduled list
        for f in self.scheduled_flights:
            if f.flight_number == number:
                f.status = 'Cancelled'
                self.scheduled_flights.remove(f)
                self.canceled_flights.append(f)
                print(f"Canceled: {number}")
                return
        # On runway
        for r in self.runways:
            if not r.is_available and r.current_flight.flight_number == number:
                f = r.release_runway()
                self.canceled_flights.append(f)
                print(f"Canceled from runway: {number}")
                return
        print("Flight not found.")

    def undo_cancellation(self):
        """Restore the last canceled flight."""
        if self.canceled_flights:
            f = self.canceled_flights.pop()
            self.scheduled_flights.append(f)
            print(f"Restored: {f}")
        else:
            print("No canceled flights to restore.")

    # ---------------- STATUS ----------------
    def show_status(self):
        """Show system summary."""
        print("\nSystem Status")
        print(f" Scheduled: {len(self.scheduled_flights)}")
        print(f" Canceled: {len(self.canceled_flights)}")
        print(f" Free Runways: {sum(r.is_available for r in self.runways)}")

        if self.scheduled_flights:
            print(" Flights waiting:")
            for f in self.scheduled_flights:
                print("  -", f)

        if self.canceled_flights:
            print(" Recently canceled:")
            for f in self.canceled_flights[-3:]:
                print("  -", f)
    def show_status_list(self):
        return {'scheduled flights':self.scheduled_flights,
                'cancelled flights':self.canceled_flights,
                'runways':self.runways}
    def get_scheduled_flights(self):
        return self.scheduled_flights


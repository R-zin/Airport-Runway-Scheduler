"""
Demo script for Airport Management System
This script demonstrates all the features without requiring user input.
"""

from AirportManagementSystem import AirportManagementSystem
from datetime import datetime, timedelta

def run_demo():
    """Run a demonstration of the Airport Management System."""
    print("🛫 Airport Management System - Demo")
    print("=" * 50)
    
    # Create the system
    system = AirportManagementSystem()
    
    print("\n1. Adding sample flights...")
    # Add some sample flights
    system.add_flight("AA101", "LAX", "08:30", False)  # Normal flight
    system.add_flight("EM201", "LHR", "09:00", True)   # Emergency flight
    system.add_flight("UA301", "SFO", "10:15", False)  # Normal flight
    system.add_flight("DL401", "CDG", "11:45", False)  # Normal flight
    
    print("\n2. Scheduling flights...")
    system.schedule_flights()
    
    print("\n3. Allocating runways...")
    system.allocate_runway()
    
    print("\n4. Finding routes between airports...")
    system.find_route("JFK", "NRT")
    system.find_route("LAX", "FRA")
    system.find_route("JFK", "XYZ")  # Non-existent route
    
    print("\n5. Displaying system status...")
    system.display_status()
    
    print("\n6. Canceling a flight...")
    system.cancel_flight("UA301")
    
    print("\n7. Undoing last cancellation...")
    system.undo_last_cancellation()
    
    print("\n8. Final system status...")
    system.display_status()
    
    print("\n" + "=" * 50)
    print("Demo completed! ✈️")
    print("\nTo run the interactive version, use: python main.py")

if __name__ == "__main__":
    run_demo()

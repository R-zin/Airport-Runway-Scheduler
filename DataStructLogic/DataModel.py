# BackEnd/DataStructLogic/DataModel.py

class Flight:
    def __init__(self, flight_number, dst, distance, fuel_load, type, Emergency, Operation_mode):
        self.flight_number = flight_number
        self.dst = dst
        self.distance = distance
        self.fuel_load = fuel_load
        self.type = type
        self.Emergency = Emergency
        self.Operation_mode = Operation_mode

    def priority(self):
        """
        Compute flight priority based on Emergency and fuel_load.
        Lower numbers = higher priority in PriorityQueue.
        """
        if self.Emergency:
            return 0  # Emergency flights always top
        return self.fuel_load  # Otherwise prioritize low fuel load

    def __str__(self):
        return (f"Flight {self.flight_number} → {self.dst} | "
                f"Fuel: {self.fuel_load} | Type: {self.type} | "
                f"Emergency: {self.Emergency} | Mode: {self.Operation_mode}")

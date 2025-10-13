from pydantic import BaseModel

class add_flights(BaseModel):
    flight_no:str
    destination:str
    time_str:str
    is_emergency:bool
class cancel_flight(BaseModel):
    flight_no:str
class route_add(BaseModel):
    src:str
    dest:str
    distance:int
class route_find_data(BaseModel):
    src:str
    dest:str

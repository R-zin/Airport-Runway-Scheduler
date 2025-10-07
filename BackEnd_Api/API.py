
from AirportManagementSystem import Managmement_System
from fastapi import FastAPI,HTTPException
from BackEnd_Api.DataModels import *
management_system = Managmement_System()
app = FastAPI()


@app.post('/flights/add_flight')
def add_plane(data:add_flights):
    try:
        management_system.add_flight(data.flight_no,data.destination,data.time_str,data.is_emergency)
        management_system.schedule_flights()
        return {'status':f'flight No {data.flight_no} added successfully'}
    except Exception as e:
        raise HTTPException(status_code=500,detail='flight adding failed')
@app.post('/route/add_route')
def add_route(data:route_add):
    try:
        management_system.add_route(data.src,data.dest,data.distance)
        return {'status':'Route Added successfully'}
    except Exception as e:
        raise HTTPException(status_code=500,detail='Route adding failed')
@app.get('/flights/list_flights')
def get_flights():
    try:
        flights = management_system.get_scheduled_flights()
        flight_data = [vars(f) for f in flights]
        return {'data': flight_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error fetching flights: {str(e)}')
@app.get('/flights/assign_runway')
def runway_allocation():
    management_system.allocate_runways()








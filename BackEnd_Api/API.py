
from AirportManagementSystem import Managmement_System
from fastapi import FastAPI,HTTPException
from BackEnd_Api.DataModels import *
management_system = Managmement_System()
app = FastAPI()


@app.post('/flights/add_flight')
def add_plane(data:add_flights):
    try:
        management_system.add_flight(data.flight_no,data.destination,data.time_str,data.is_emergency)
        return {'status':'Success'}
    except Exception as e:
        raise HTTPException(status_code=500,detail='flight adding failed')




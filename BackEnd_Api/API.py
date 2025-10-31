from datetime import time
from AirportManagementSystem import Managmement_System
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from BackEnd_Api.DataModels import *

management_system = Managmement_System()
app = FastAPI()

# CORS for local development and potential deployment origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/flights/add_flight')
def add_plane(data:add_flights):
    try:
        management_system.add_flight(data.flight_no,data.destination,data.time_str,data.is_emergency)
        management_system.schedule_flights()
        return {'status':f'flight No {data.flight_no} added successfully'}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'flight adding failed {str(e)}')
@app.post('/flights/cancel_flight')
def cancel(data:cancel_flight):
    try:
        management_system.cancel_flight(data.flight_no)
        return {'status':f'flight {data.flight_no} cancelled'}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'flight could not be cancelled {str(e)}')
@app.get('/flights/cancelled_list')
def get_cancelled_list():
    try:
        flights = management_system.canceled_flights
        flight_data = [
            FlightResponse(
                flight_no=f.flight_number,
                destination=f.destination,
                departure_time=f.departure_time.strftime("%H:%M"),
                status=f.status,
                assigned_runway=f.assigned_runway_no,
                Emergency_flight=f.is_emergency
            )
            for f in flights
        ]
        return {'cancelled_list': flight_data}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'Could not retrive cancelled flights {str(e)}')

@app.post('/route/add_route')
def add_route(data:route_add):
    try:
        management_system.add_route(data.src,data.dest,data.distance)
        return {'status':'Route Added successfully'}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'Route adding failed {str(e)}')

@app.post('/route/find_route')
def findroute(data:route_find_data):
    try:
        path,distance = management_system.airport_graph.find_shortest_route(data.src,data.dest)
        return {
            'Path':path,
            'Distance':distance
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'Could not find the route {str(e)}')
@app.get('/flights/list_scheduled_flights')
def get_flights():
    try:
        flights = management_system.get_scheduled_flights()
        flight_data = [vars(f) for f in flights]
        return {'data': flight_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error fetching flights: {str(e)}')
@app.get('/flight/get_all_flights')
def list_all():
    try:
        flights = management_system.history
        flight_data = [
            FlightResponse(
                flight_no=f.flight_number,
                destination=f.destination,
                departure_time=f.departure_time.strftime("%H:%M"),
                status=f.status,
                assigned_runway=f.assigned_runway_no,
                Emergency_flight=f.is_emergency
            )
            for f in flights
        ]
        return {'data':flight_data}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'Error getting history flights {str(e)}')
@app.get('/flights/assign_runway')
def runway_allocation():
    try:
        management_system.allocate_runways()
        return {'status':'Allocation successful'}
    except Exception as e:
        raise  HTTPException(status_code=500,detail=f'runway allocation failed {str(e)}')
@app.get('/runways/status')
def runway_info():
    try:
        runways = management_system.runways
        lst = [RunwayResponse(
            runway_no=r.runway_id,
            flight_no=r.current_flight_name
        )for r in runways]
        return {
            'data':lst
        }
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'COuld,nt get info {str(e)}')
@app.get('/runways/clear_departed')
def clear_departed():
    try:
        management_system._clear_departed_flights()
        return {"Status": "Succesfully cleared departed flights"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Couldnt automcatically clear runway {str(e)}")













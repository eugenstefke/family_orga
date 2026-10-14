from auth.auth_users import get_current_user
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from schema_event import EventCreate, EventOut, EventDetail, AllEventsOut, EventUpdate, EventDelete
from datamanager_event import DataManagerEvent
from models.models import User
from database import get_db
app = FastAPI()

@app.get("/event/{event_id}", response_model=EventDetail)
def read_event_details(event_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, event_details = DataManagerEvent().get_event_details(event_id, current_user, db)
    if message:
        raise HTTPException(status_code=404, detail=message)
    return event_details

@app.get("/get/all/events", response_model=list[AllEventsOut])
def read_events(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    events = DataManagerEvent().get_events(current_user, db)
    return events

@app.post("/event/create", response_model=EventOut)
def create_event(event_details: EventCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, event = DataManagerEvent().add_event(event_details, current_user, db)
    if message:
        raise HTTPException(status_code=400, detail=message)

    return EventOut(message=f"{event.title} on {event.date_time} added")

@app.put("/event/{event_id}", response_model=EventUpdate)
def update_event(event_id: int, event: EventCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, event = DataManagerEvent().update_event(event_id, current_user, event, db)
    if message:
        raise HTTPException(status_code=400, detail=message)
    return EventUpdate(message=f"The changes made for the {event.title} event were successfull")

@app.delete("/event/{event_id}", response_model=EventDelete)
def delete_event(event_id: int, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    message, event = DataManagerEvent().delete_event(event_id, current_user, db)

    if message:
        raise HTTPException(status_code=400, detail=message)

    return EventDelete(message=f"{event} is no longer in your list")
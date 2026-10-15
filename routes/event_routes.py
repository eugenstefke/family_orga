from auth.auth_users import get_current_user
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.schema_event import EventCreate, EventOut, EventDetail, AllEventsOut, EventUpdate, EventDelete
from models.models import User
from data.database import get_db
from repositories.event_repository_sqlalchemy import EventRepositorySqlalchemy
from services.event_service import EventService

router = APIRouter()

@router.get("/event/{event_id}", response_model=EventDetail)
def read_event_details(event_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = EventRepositorySqlalchemy(session=db)
    service = EventService(repository=repository)
    message, event_details = service.get_event_details(event_id, current_user)

    if message:
        raise HTTPException(status_code=404, detail=message)
    return event_details

@router.get("/get/all/events", response_model=list[AllEventsOut])
def read_events(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = EventRepositorySqlalchemy(session=db)
    service = EventService(repository=repository)
    events = service.get_events(current_user)
    return events

@router.post("/event/create", response_model=EventOut)
def create_event(event_details: EventCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = EventRepositorySqlalchemy(session=db)
    service = EventService(repository=repository)
    message, event = service.add_event(event_details, current_user)
    if message:
        raise HTTPException(status_code=400, detail=message)

    return EventOut(message=f"{event.title} on {event.date_time} added")

@router.put("/event/{event_id}", response_model=EventUpdate)
def update_event(event_id: int, event_details: EventCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = EventRepositorySqlalchemy(session=db)
    service = EventService(repository=repository)
    message, event = service.update_event(event_id, current_user, event_details)

    if message:
        raise HTTPException(status_code=400, detail=message)
    return EventUpdate(message=f"The changes made for the {event.title} event were successfull")

@router.delete("/event/{event_id}", response_model=EventDelete)
def delete_event(event_id: int, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    repository = EventRepositorySqlalchemy(session=db)
    service = EventService(repository=repository)
    message, event = service.delete_event(event_id, current_user)

    if message:
        raise HTTPException(status_code=400, detail=message)

    return EventDelete(message=f"{event} is no longer in your list")
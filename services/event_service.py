from repositories.event_repository import IEventRepository
from schemas.schema_event import EventCreate
from models.models import User, Event

class EventService:
    """Business logic for events.
    Works with any repository that implements IEventRepository,
    so the database access can be exchanged without changing the service."""

    def __init__(self, repository: IEventRepository):
        """Initialize the service with the repository used for event data access."""
        self.repository = repository

    def get_event_details(self, event_id: int, current_user: User,):
        """Return the event with the given ID if it belongs to the user.
        Return (None, event) on success
        If the event not found, return (“Event not found”, None)."""

        event = self.repository.get_by_id(owner_id=current_user.id, event_id=event_id)

        if not event:
            return "Event not found", None

        return None, event

    def get_events(self, current_user:User):
        """Returns all events of the given user as a list"""
        events = self.repository.get_all(owner_id=current_user.id)
        return events

    def add_event(self, event_details: EventCreate, current_user: User):
        """Create event for the given user and link the event to the given familymembers.

        Return (None, new_event) on success.
        Return (message, None) if a familymember ID does not exist or does not
        belong to the user. In that case nothing is saved."""

        new_event = Event(
            title=event_details.title,
            date_time=event_details.date_time,
            location=event_details.location,
            category=event_details.category,
            owner_id=current_user.id
        )

        self.repository.add_event(new_event)
        #ensures that new_event is now set to DB.
        #Otherwise, the validation of the family member IDs cannot take place, as there is currently nothing in the database without a flush()
        self.repository.flush()

        valid_familymembers = self.repository.validation(event_details=event_details, current_user=current_user)

        valid_ids = {familymember.id for familymember in valid_familymembers}
        for familymember_id in set(event_details.familymember_id):
            if familymember_id not in valid_ids:
                return f"Invalid familymember id: {familymember_id}", None
            self.repository.add_linking(familymember_id=familymember_id, event_id=new_event.id)

        self.repository.commit()

        return None, new_event

    def update_event(self, event_id: int, current_user: User, event_details: EventCreate):
        """Update the event with the given ID and replace its familymember links.

        Return (None, None, event) on success
        If the event not found, return (404, “Event not found”, None).
        Return (400, message, None) if a familymember ID does not exist or does not belong to the user.
        In that case nothing is saved."""

        event = self.repository.get_by_id(owner_id=current_user.id, event_id=event_id)

        if not event:
            return 404, "Event not found", None

        valid_familymembers = self.repository.validation(event_details=event_details, current_user=current_user)

        valid_ids = {familymember.id for familymember in valid_familymembers}
        for familymember_id in set(event_details.familymember_id):
            if familymember_id not in valid_ids:
                return 400, f"Invalid familymember id: {familymember_id}", None

        event.title = event_details.title
        event.date_time = event_details.date_time
        event.location = event_details.location
        event.category = event_details.category

        self.repository.delete_linking(event_id=event_id)  # alte Zuordnungen entfernen
        for familymember_id in set(event_details.familymember_id):
            self.repository.add_linking(familymember_id=familymember_id, event_id=event_id)

        self.repository.commit()
        return None, None, event

    def delete_event(self, event_id: int, current_user: User):
        """Delete event with the given event id and user.
        Return (None, event_title) on success
        If the doctor not found, return (“Event not found”, None)."""

        event_to_delete = self.repository.get_by_id(owner_id=current_user.id, event_id=event_id)

        if not event_to_delete:
            return "Event not found", None

        delete_title = event_to_delete.title # keep the title for the response, the event is deleted afterwards

        self.repository.delete_event(event_to_delete)
        self.repository.commit()

        return None, delete_title
from repositories.event_repository import IEventRepository
from schemas.schema_event import EventCreate
from models.models import User, Event

class EventService:

    def __init__(self, repository: IEventRepository):
        self.repository = repository

    def get_event_details(self, event_id: int, current_user: User,):

        event = self.repository.get_by_id(owner_id=current_user.id, event_id=event_id)

        if not event:
            return "Event not found", None

        return None, event

    def get_events(self, current_user:User):

        events = self.repository.get_all(owner_id=current_user.id)
        return events

    def add_event(self, event_details: EventCreate, current_user: User):

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
        for familymember_id in event_details.familymember_id:
            if familymember_id not in valid_ids:
                return f"Invalid familymember id: {familymember_id}", None
            self.repository.add_linking(familymember_id=familymember_id, event_id=new_event.id)

        self.repository.commit()

        return None, new_event

    def update_event(self, event_id: int, current_user: User, event_details: EventCreate):

        event = self.repository.get_by_id(owner_id=current_user.id, event_id=event_id)

        if not event:
            return 404, "Event not found", None

        valid_familymembers = self.repository.validation(event_details=event_details, current_user=current_user)

        valid_ids = {familymember.id for familymember in valid_familymembers}
        for familymember_id in event_details.familymember_id:
            if familymember_id not in valid_ids:
                return 400, f"Invalid familymember id: {familymember_id}", None

        event.title = event_details.title
        event.date_time = event_details.date_time
        event.location = event_details.location
        event.category = event_details.category

        self.repository.delete_linking(event_id=event_id)  # alte Zuordnungen entfernen
        for familymember_id in event_details.familymember_id:
            self.repository.add_linking(familymember_id=familymember_id, event_id=event_id)

        self.repository.commit()
        return None, None, event

    def delete_event(self, event_id: int, current_user: User):

        event_to_delete = self.repository.get_by_id(owner_id=current_user.id, event_id=event_id)

        if not event_to_delete:
            return "Event not found", None

        delete_title = event_to_delete.title # for save the title of delete event

        self.repository.delete_event(event_to_delete)
        self.repository.commit()

        return None, delete_title
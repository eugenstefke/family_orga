from schema_event import EventCreate
from models import User, Event, FamilymemberEvent, FamilyMember
from sqlalchemy.orm import Session

class DataManagerEvent:

    def add_event(self, event_details: EventCreate, current_user: User, db: Session):

        new_event = Event(
            title=event_details.title,
            date_time=event_details.date_time,
            location=event_details.location,
            category=event_details.category,
            owner_id=current_user.id
        )

        db.add(new_event)
        #ensures that new_event is now set to DB.
        #Otherwise, the validation of the family member IDs cannot take place, as there is currently nothing in the database without a flush()
        db.flush()

        valid_family_members = db.query(FamilyMember).filter(FamilyMember.id.in_(event_details.familymember_id), FamilyMember.owner_id == current_user.id).all()

        valid_ids = {familymember.id for familymember in valid_family_members}
        for familymember_id in event_details.familymember_id:
            if familymember_id not in valid_ids:
                return f"Invalid familymember id: {familymember_id}", None
            table_linking = FamilymemberEvent(
                familymember_id=familymember_id,
                event_id=new_event.id
            )
            db.add(table_linking)

        db.commit()

        return None, new_event

    def get_event_details(self, event_id: int, current_user: User, db: Session):

        event = db.query(Event).filter_by(owner_id=current_user.id, id=event_id).first()

        if not event:
            return "Event not found", None

        return None, event

    def get_events(self, current_user:User, db: Session):

        events = db.query(Event).filter_by(owner_id=current_user.id).all()
        return events

    def update_event(self, event_id: int, current_user: User, event: EventCreate, db: Session):

        new_event = db.query(Event).filter_by(owner_id=current_user.id, id=event_id).first()

        if not new_event:
            return "Event not found", None

        valid_family_members = db.query(FamilyMember).filter(FamilyMember.id.in_(event.familymember_id),
                                                             FamilyMember.owner_id == current_user.id).all()

        valid_ids = {familymember.id for familymember in valid_family_members}
        for familymember_id in event.familymember_id:
            if familymember_id not in valid_ids:
                return f"Invalid familymember id: {familymember_id}", None

        new_event.title = event.title
        new_event.date_time = event.date_time
        new_event.location = event.location
        new_event.category = event.category

        db.query(FamilymemberEvent).filter_by(event_id=event_id).delete()  # alte Zuordnungen entfernen
        for familymember_id in event.familymember_id:
            db.add(FamilymemberEvent(familymember_id=familymember_id, event_id=event_id))

        db.commit()
        return None, new_event

    def delete_event(self, event_id: int, current_user: User, db: Session):

        event_to_delete = db.query(Event).filter_by(owner_id=current_user.id, id=event_id).first()

        if not event_to_delete:
            return "Event not found", None

        delete_title = event_to_delete.title # for save the title of delete event

        db.delete(event_to_delete)
        db.commit()

        return None, delete_title
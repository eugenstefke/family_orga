from repositories.event_repository import IEventRepository
from sqlalchemy.orm import Session
from models.models import Event, FamilymemberEvent, FamilyMember

class EventRepositorySqlalchemy(IEventRepository):
    """Child class of IEventRepository that implements its methods"""

    def __init__(self, session: Session):
        """Store the database session that is shared across the request"""
        self.db = session

    def get_by_id(self, owner_id, event_id):
        """Returns a event based on their ID and the owner ID"""
        return self.db.query(Event).filter_by(owner_id=owner_id, id=event_id).first()

    def get_all(self, owner_id):
        """Return all events that belong to the given owner."""
        return self.db.query(Event).filter_by(owner_id=owner_id).all()

    def add_event(self, new_event):
        """Stage a new event for insertion"""
        self.db.add(new_event)

    def flush(self):
        """Flush pending changes to the database so generated IDs are available"""
        self.db.flush()

    def validation(self, event_details, current_user):
        """Returns those of the requested family members that belong to the current user"""
        return self.db.query(FamilyMember).filter(FamilyMember.id.in_(event_details.familymember_id),FamilyMember.owner_id == current_user.id).all()

    def add_linking(self, familymember_id, event_id):
        """Set up a link between a family member and event in the links table"""
        self.db.add(FamilymemberEvent(familymember_id=familymember_id, event_id=event_id))

    def commit(self):
        """Make all pending changes permanent"""
        self.db.commit()

    def delete_linking(self, event_id):
        """Delete all link entries of the given event"""
        self.db.query(FamilymemberEvent).filter_by(event_id=event_id).delete()

    def delete_event(self, event):
        """Deletes event"""
        self.db.delete(event)

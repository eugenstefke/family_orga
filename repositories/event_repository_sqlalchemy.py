from event_repository import IEventRepository
from sqlalchemy.orm import Session
from models.models import Event, FamilymemberEvent, FamilyMember

class EventRepositorySqlalchemy(IEventRepository):

    def __init__(self, session: Session):
        self.db = session

    def get_by_id(self, owner_id, event_id):

        return self.db.query(Event).filter_by(owner_id=owner_id, id=event_id).first()

    def get_all(self, owner_id):

        return self.db.query(Event).filter_by(owner_id=owner_id).all()

    def add_event(self, new_event):
        self.db.add(new_event)

    def flush(self):
        self.db.flush()

    def validation(self, event_details, current_user):
        return self.db.query(FamilyMember).filter(FamilyMember.id.in_(event_details.familymember_id),FamilyMember.owner_id == current_user.id).all()

    def add_linking(self, familymember_id, event_id):
        self.db.add(FamilymemberEvent(familymember_id=familymember_id, event_id=event_id))

    def commit(self):
        self.db.commit()

    def delete_linking(self, event_id):
        self.db.query(FamilymemberEvent).filter_by(event_id=event_id).delete()

    def delete_event(self, event):
        self.db.delete(event)

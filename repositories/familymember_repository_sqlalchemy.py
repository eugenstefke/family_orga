from sqlalchemy.orm import Session
from familymember_repository import IFamilyMemberRepository
from models.models import FamilyMember

class FamilyMemberRepositorySqlalchemy(IFamilyMemberRepository):

    def __init__(self, session: Session):
        self.db = session

    def get_all(self, owner_id):
        return self.db.query(FamilyMember).filter_by(owner_id=owner_id).all()

    def get_by_id(self, owner_id, familymember_id):
        return self.db.query(FamilyMember).filter_by(owner_id=owner_id, id=familymember_id).first()

    def familymember_existing(self, familymember_name, familymember_birthday, owner_id):
        return self.db.query(FamilyMember).filter_by(name=familymember_name, birthday=familymember_birthday, owner_id=owner_id).first()

    def add_familymember(self, new_familymember):
        self.db.add(new_familymember)

    def commit(self):
        self.db.commit()

    def delete_familymember(self, familymember):
        self.db.delete(familymember)
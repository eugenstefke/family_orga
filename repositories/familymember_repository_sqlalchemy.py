from sqlalchemy.orm import Session
from repositories.familymember_repository import IFamilyMemberRepository
from models.models import FamilyMember

class FamilyMemberRepositorySqlalchemy(IFamilyMemberRepository):
    """Child class of IFamilyMemberRepository that implements its methods"""

    def __init__(self, session: Session):
        """Store the database session that is shared across the request"""
        self.db = session

    def get_all(self, owner_id):
        """Return all familymember that belong to the given owner."""
        return self.db.query(FamilyMember).filter_by(owner_id=owner_id).all()

    def get_by_id(self, owner_id, familymember_id):
        """Returns familymember based on their ID and the owner ID"""
        return self.db.query(FamilyMember).filter_by(owner_id=owner_id, id=familymember_id).first()

    def familymember_existing(self, familymember_name, familymember_birthday, owner_id):
        """ Return the family member matching name, birthday, or None if there is none.
        Used to detect duplicates; the birthday is included so twins with the same name are not blocked """

        return self.db.query(FamilyMember).filter_by(name=familymember_name, birthday=familymember_birthday, owner_id=owner_id).first()

    def add_familymember(self, new_familymember):
        """Stage a new familymember for insertion"""
        self.db.add(new_familymember)

    def commit(self):
        """Make all pending changes permanent"""
        self.db.commit()

    def delete_familymember(self, familymember):
        """Deletes a familymember"""
        self.db.delete(familymember)
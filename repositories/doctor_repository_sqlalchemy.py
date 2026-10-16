from sqlalchemy.orm import Session
from repositories.doctor_repository import IDoctorRepository
from models.models import FamilyMember, Doctor, FamilymemberDoctor

class DoctorRepositorySqlalchemy(IDoctorRepository):
    """Child class of IDoctorRepository that implements its methods"""

    def  __init__ (self, session: Session ):
        """Store the database session that is shared across the request"""
        self.db = session

    def add_doctor(self, new_doctor):
        """Stage a new doctor for insertion"""
        self.db.add(new_doctor)

    def add_linking(self, familymember_id, doctor_id):
        """Set up a link between a family member and a doctor in the links table"""
        self.db.add(FamilymemberDoctor(familymember_id=familymember_id, doctor_id=doctor_id))

    def flush(self):
        """Flush pending changes to the database so generated IDs are available"""
        self.db.flush()

    def validation(self, doctor_details, current_user):
        """Returns those of the requested family members that belong to the current user"""
        return self.db.query(FamilyMember).filter(FamilyMember.id.in_(doctor_details.familymember_id), FamilyMember.owner_id == current_user.id).all()

    def commit(self):
        """Make all pending changes permanent"""
        self.db.commit()

    def get_by_id(self, owner_id, doctor_id):
        """Returns a doctor based on their ID and the owner ID"""
        return self.db.query(Doctor).filter_by(owner_id=owner_id, id=doctor_id).first()

    def get_all(self, owner_id):
        """Return all doctors that belong to the given owner."""
        return self.db.query(Doctor).filter_by(owner_id=owner_id).all()

    def delete_doctor(self, owner_id, doctor_id):
        """Deletes a doctor using their ID and the owner ID """
        self.db.query(Doctor).filter_by(owner_id=owner_id, id=doctor_id).delete()

    def delete_linking(self, doctor_id):
        """Delete all link entries of the given doctor"""
        self.db.query(FamilymemberDoctor).filter_by(doctor_id=doctor_id).delete()
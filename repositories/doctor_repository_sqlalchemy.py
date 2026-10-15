from sqlalchemy.orm import Session
from repositories.doctor_repository import IDoctorRepository
from models.models import FamilyMember, Doctor, FamilymemberDoctor

class DoctorRepositorySqlalchemy(IDoctorRepository):
    def  __init__ (self, session: Session ):
        self.db = session

    def add_doctor(self, new_doctor):

        if new_doctor:
            self.db.add(new_doctor)

    def add_linking(self, familymember_id, doctor_id):
        self.db.add(FamilymemberDoctor(familymember_id=familymember_id, doctor_id=doctor_id))

    def cache(self):
        self.db.flush()

    def validation(self, doctor_details, current_user):
        return self.db.query(FamilyMember).filter(FamilyMember.id.in_(doctor_details.familymember_id), FamilyMember.owner_id == current_user.id).all()

    def commit(self):
        self.db.commit()

    def get_by_id(self, owner_id, doctor_id):
        return self.db.query(Doctor).filter_by(owner_id=owner_id, id=doctor_id).first()

    def get_all(self, owner_id):
        return self.db.query(Doctor).filter_by(owner_id=owner_id).all()

    def delete_doctor(self, owner_id, doctor_id):
        self.db.query(Doctor).filter_by(owner_id=owner_id, id=doctor_id).delete()

    def delete_linking(self, doctor_id):
        self.db.query(FamilymemberDoctor).filter_by(doctor_id=doctor_id).delete()
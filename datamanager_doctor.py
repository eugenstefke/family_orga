from schema_doctor import DoctorCreate
from models import Doctor, FamilymemberDoctor
from models import User, FamilymemberEvent, FamilyMember, FamilymemberDoctor
from sqlalchemy.orm import Session

class DataManagerDoctor:

    def add_new_doctor(self, doctor_details: DoctorCreate, current_user: User, db: Session):

        new_doctor = Doctor(
            name=doctor_details.name,
            field_of_study=doctor_details.field_of_study,
            contact_details=doctor_details.contact_details,
            owner_id=current_user.id
        )

        db.add(new_doctor)
        #ensures that new_doctor is now set to DB.
        #Otherwise, the validation of the family member IDs cannot take place, as there is currently nothing in the database without a flush()
        db.flush()

        valid_family_members = db.query(FamilyMember).filter(FamilyMember.id.in_(doctor_details.familymember_id), FamilyMember.owner_id == current_user.id).all()

        valid_ids = {familymember.id for familymember in valid_family_members}
        for familymember_id in doctor_details.familymember_id:
            if familymember_id not in valid_ids:
                return f"Invalid familymember id: {familymember_id}", None
            table_linking = FamilymemberDoctor(
                familymember_id=familymember_id,
                doctor_id=new_doctor.id
            )
            db.add(table_linking)

        db.commit()

        return None, new_doctor

    def get_doctor_details(self, doctor_id: int, current_user: User, db: Session):

        doctor = db.query(Doctor).filter_by(owner_id=current_user.id, id=doctor_id).first()

        if not doctor:
            return "Doctor not found", None

        return None, doctor

    def get_doctors(self, current_user:User, db: Session):

        doctors = db.query(Doctor).filter_by(owner_id=current_user.id).all()
        return doctors

    def update_doctor(self, doctor_id: int, current_user: User, doctor_update: DoctorCreate, db: Session):

        doctor = db.query(Doctor).filter_by(owner_id=current_user.id, id=doctor_id).first()

        if not doctor:
            return "Doctor not found", None

        valid_family_members = db.query(FamilyMember).filter(FamilyMember.id.in_(doctor_update.familymember_id), FamilyMember.owner_id == current_user.id).all()

        valid_ids = {familymember.id for familymember in valid_family_members}
        for familymember_id in doctor_update.familymember_id:
            if familymember_id not in valid_ids:
                return f"Invalid familymember id: {familymember_id}", None

        doctor.name = doctor_update.name
        doctor.field_of_study = doctor_update.field_of_study
        doctor.contact_details = doctor_update.contact_details

        db.query(FamilymemberDoctor).filter_by(doctor_id=doctor_id).delete()  # alte Zuordnungen entfernen
        for familymember_id in doctor_update.familymember_id:
            db.add(FamilymemberDoctor(familymember_id=familymember_id, event_id=doctor_id))

        db.commit()
        return None, doctor

    def delete_doctor(self, doctor_id: int, current_user: User, db: Session):

        doctor_to_delete = db.query(Doctor).filter_by(owner_id=current_user.id, id=doctor_id).first()

        if not doctor_to_delete:
            return "Doctor not found", None

        delete_name = doctor_to_delete.name # for save the name of delete doctor

        db.delete(doctor_to_delete)
        db.commit()

        return None, delete_name
from repositories.doctor_repository import IDoctorRepository
from schema_doctor import DoctorCreate
from models.models import User, Doctor, FamilymemberDoctor

class DoctorServie:

    def __init__(self, repository: IDoctorRepository):
        self.repository = repository

    def add_new_doctor(self, doctor_details: DoctorCreate, current_user: User):

        new_doctor = Doctor(
            name=doctor_details.name,
            field_of_study=doctor_details.field_of_study,
            contact_details=doctor_details.contact_details,
            owner_id=current_user.id
        )

        self.repository.add_doctor(new_doctor=new_doctor)
        # ensures that new_doctor is now set to DB.
        # Otherwise, the validation of the family member IDs cannot take place, as there is currently nothing in the database without a flush() (self.repository.cache())
        self.repository.cache()

        valid_family_members = self.repository.validation(doctor_details, current_user)

        valid_ids = {familymember.id for familymember in valid_family_members}
        for familymember_id in doctor_details.familymember_id:
            if familymember_id not in valid_ids:
                return f"Invalid familymember id: {familymember_id}", None
            self.repository.add_linking(familymember_id=familymember_id, doctor_id=new_doctor.id)


        self.repository.commit()
        return None, new_doctor

    def get_doctor_details(self, doctor_id: int, current_user: User):

        doctor = self.repository.get_by_id(owner_id=current_user.id, doctor_id=doctor_id)

        if not doctor:
            return "Doctor not found", None

        return None, doctor

    def get_doctors(self, current_user:User):

        doctors = self.repository.get_all(owner_id=current_user.id)
        return doctors

    def update_doctor(self, doctor_id: int, current_user: User, doctor_details: DoctorCreate):

        doctor = self.repository.get_by_id(owner_id=current_user.id, doctor_id=doctor_id)

        if not doctor:
            return "Doctor not found", None

        valid_family_members = self.repository.validation(doctor_details, current_user)

        valid_ids = {familymember.id for familymember in valid_family_members}
        for familymember_id in doctor_details.familymember_id:
            if familymember_id not in valid_ids:
                return f"Invalid familymember id: {familymember_id}", None

        doctor.name = doctor_details.name
        doctor.field_of_study = doctor_details.field_of_study
        doctor.contact_details = doctor_details.contact_details

        self.repository.delete_linking(doctor_id=doctor_id) # alte Zuordnungen von Verknüpfungstabelle entfernen
        for familymember_id in doctor_details.familymember_id:
            self.repository.add_linking(familymember_id=familymember_id, doctor_id=doctor_id)

        self.repository.commit()
        return None, doctor


    def delete_doctor(self, doctor_id: int, current_user: User):

        doctor_to_delete = self.repository.get_by_id(owner_id=current_user.id, doctor_id=doctor_id)

        if not doctor_to_delete:
            return "Doctor not found", None

        delete_name = doctor_to_delete.name # for save the name of delete doctor

        self.repository.delete_doctor(owner_id=current_user.id, doctor_id=doctor_id)
        self.repository.commit()

        return None, delete_name
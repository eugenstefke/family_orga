from repositories.doctor_repository import IDoctorRepository
from schemas.schema_doctor import DoctorCreate
from models.models import User, Doctor

class DoctorService:
    """Business logic for doctors.
    Works with any repository that implements IDoctorRepository,
    so the database access can be exchanged without changing the service."""

    def __init__(self, repository: IDoctorRepository):
        """Initialize the service with the repository used for doctor data access."""
        self.repository = repository

    def add_new_doctor(self, doctor_details: DoctorCreate, current_user: User):
        """Create a doctor for the given user and link the doctor to the given familymembers.

        Return (None, doctor) on success.
        Return (message, None) if a familymember ID does not exist or does not
        belong to the user. In that case nothing is saved."""

        new_doctor = Doctor(
            name=doctor_details.name,
            field_of_study=doctor_details.field_of_study,
            contact_details=doctor_details.contact_details,
            owner_id=current_user.id
        )

        self.repository.add_doctor(new_doctor=new_doctor)
        # ensures that new_doctor is now written to DB.
        # Otherwise, the validation of the family member IDs cannot take place, as there is currently nothing in the database without a flush()
        self.repository.flush()

        valid_familymembers = self.repository.validation(doctor_details, current_user)

        valid_ids = {familymember.id for familymember in valid_familymembers}
        for familymember_id in set(doctor_details.familymember_id):
            if familymember_id not in valid_ids:
                return f"Invalid familymember id: {familymember_id}", None
            self.repository.add_linking(familymember_id=familymember_id, doctor_id=new_doctor.id)


        self.repository.commit()
        return None, new_doctor

    def get_doctor_details(self, doctor_id: int, current_user: User):
        """Return the doctor with the given ID if it belongs to the user.
        Return (None, doctor) on success
        If the doctor not found, return (“Doctor not found”, None)."""

        doctor = self.repository.get_by_id(owner_id=current_user.id, doctor_id=doctor_id)

        if not doctor:
            return "Doctor not found", None

        return None, doctor

    def get_doctors(self, current_user:User):
        """Returns all doctors of the given user as a list"""
        doctors = self.repository.get_all(owner_id=current_user.id)
        return doctors

    def update_doctor(self, doctor_id: int, current_user: User, doctor_details: DoctorCreate):
        """Update the doctor with the given ID and replace its familymember links.

        Return (None, None, doctor) on success
        If the doctor not found, return (404, “Doctor not found”, None).
        Return (400, message, None) if a familymember ID does not exist or does not belong to the user.
        In that case nothing is saved."""

        doctor = self.repository.get_by_id(owner_id=current_user.id, doctor_id=doctor_id)

        if not doctor:
            return 404, "Doctor not found", None

        valid_familymembers = self.repository.validation(doctor_details, current_user)

        valid_ids = {familymember.id for familymember in valid_familymembers}
        for familymember_id in set(doctor_details.familymember_id):
            if familymember_id not in valid_ids:
                return 400, f"Invalid familymember id: {familymember_id}", None

        doctor.name = doctor_details.name
        doctor.field_of_study = doctor_details.field_of_study
        doctor.contact_details = doctor_details.contact_details

        self.repository.delete_linking(doctor_id=doctor_id) # Remove old mappings from the join table
        for familymember_id in set(doctor_details.familymember_id):
            self.repository.add_linking(familymember_id=familymember_id, doctor_id=doctor_id)

        self.repository.commit()
        return None, None, doctor


    def delete_doctor(self, doctor_id: int, current_user: User):
        """Delete doctor with the given doctor id and user.
        Return (None, doctor_name) on success
        If the doctor not found, return (“Doctor not found”, None)."""

        doctor_to_delete = self.repository.get_by_id(owner_id=current_user.id, doctor_id=doctor_id)

        if not doctor_to_delete:
            return "Doctor not found", None

        delete_name = doctor_to_delete.name # keep the name for the response, the doctor is deleted afterwards

        self.repository.delete_doctor(doctor_to_delete)
        self.repository.commit()

        return None, delete_name
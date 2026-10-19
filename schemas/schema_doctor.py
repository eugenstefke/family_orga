from pydantic import BaseModel, Field, ConfigDict

class DoctorCreate(BaseModel):
    """Data required to create a new doctor.

    Name, field of study and contact details must not be empty.
    familymember_id lists the family members the doctor is linked to"""

    name: str = Field(min_length=1)
    field_of_study: str = Field(min_length=1)
    contact_details: str = Field(min_length=1)
    familymember_id: list[int]

class DoctorOut(BaseModel):
    """Data of a doctor, returned after the doctor has been created."""
    name: str
    field_of_study: str
    contact_details: str

    model_config = ConfigDict(from_attributes=True)

class AllDoctorsOut(BaseModel):
    """Summary of a doctor as shown in the list of all doctors."""
    id: int
    name: str
    field_of_study: str
    contact_details: str

    model_config = ConfigDict(from_attributes=True)

class FamilyMemberMiniDetails(BaseModel):
    """Minimal family member data (ID and name), shown inside the doctor details."""

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class DoctorDetail(BaseModel):
    """Details of a doctor including the family members linked to the doctor."""

    id: int
    name: str
    field_of_study: str
    contact_details: str
    family_members: list[FamilyMemberMiniDetails]

    model_config = ConfigDict(from_attributes=True)

class DoctorUpdateOut(BaseModel):
    """Confirmation message returned after a doctor has been updated."""
    message: str

class DoctorDeleteOut(BaseModel):
    """Confirmation message returned after a doctor has been deleted."""
    message: str


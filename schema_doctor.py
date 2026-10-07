from pydantic import BaseModel, Field, ConfigDict


#Output for Post request
class DoctorCreate(BaseModel):
    name: str = Field(min_length=1)
    field_of_study: str = Field(min_length=1)
    contact_details: str = Field(min_length=1)
    familymember_id: list[int]

#Output after Creat Doctor
class DoctorOut(BaseModel):

    name: str
    field_of_study: str
    contact_details: str

    model_config = ConfigDict(from_attributes=True)

#Output for get all events
class AllDoctorsOut(BaseModel):

    id: int
    name: str
    field_of_study: str
    contact_details: str

    model_config = ConfigDict(from_attributes=True)

# Mini familymember details to make the class DoctorDetail output clearer
class FamilyMemberMiniDetails(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

#Output for get request
class DoctorDetail(BaseModel):
    id: int
    name: str
    field_of_study: str
    contact_details: str
    family_members: list[FamilyMemberMiniDetails]

    model_config = ConfigDict(from_attributes=True)

#Update Outpute
class DoctorUpdate(BaseModel):

    message: str

# Output for Delete
class DoctorDelete(BaseModel):

    message: str


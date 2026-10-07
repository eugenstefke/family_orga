from datetime import datetime
from pydantic import BaseModel,  Field, ConfigDict
from typing import  Optional

#Output for Post request
class EventCreate(BaseModel):
    title: str = Field(min_length=1)
    date_time: datetime = Field(examples=["JJJJ-MM-DDTHH:MM"])
    location: str = "No location was specified"
    category: Optional[str] = None
    familymember_id: list[int]

#Output after Creat Event
class EventOut(BaseModel):

    message: str

#Output for get all events
class AllEventsOut(BaseModel):

    id: int
    title: str
    date_time: datetime
    location: str
    category: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

#Output for get request
class EventDetail(BaseModel):
    id: int
    title: str
    date_time: datetime
    location: str
    category: Optional[str] = None
    family_members: list[FamilyMemberMiniDetails]

    model_config = ConfigDict(from_attributes=True)

#Update Outpute
class EventUpdate(BaseModel):

    message: str

# Output for Delete
class EventDelete(BaseModel):

    message: str

# Mini familymember details to make the class EventDetail output clearer
class FamilyMemberMiniDetails(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
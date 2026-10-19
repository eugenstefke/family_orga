from datetime import datetime
from pydantic import BaseModel,  Field, ConfigDict
from typing import  Optional

class EventCreate(BaseModel):
    """Required details for creating a new event.

    The title field must not be empty.
    The date time must be in the format YYYY-MM-DDTHH:MM
    location has the default value: ‘No location was specified’
    category is optional
    familymember_id lists the family members attending the event"""

    title: str = Field(min_length=1)
    date_time: datetime = Field(examples=["JJJJ-MM-DDTHH:MM"])
    location: str = "No location was specified"
    category: Optional[str] = None
    familymember_id: list[int]

class EventOut(BaseModel):
    """Confirmation message returned after creat event."""
    message: str


class AllEventsOut(BaseModel):
    """Summary of an event, as displayed in the list of all events."""
    id: int
    title: str
    date_time: datetime
    location: str
    category: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class FamilyMemberMiniDetails(BaseModel):
    """Minimum details of family members (ID and name) displayed in the event data."""
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class EventDetail(BaseModel):
    """Details of a event including the family members linked to the event."""

    id: int
    title: str
    date_time: datetime
    location: str
    category: Optional[str] = None
    family_members: list[FamilyMemberMiniDetails]

    model_config = ConfigDict(from_attributes=True)


class EventUpdate(BaseModel):
    """Confirmation message returned after event has been updated."""
    message: str

# Output for Delete
class EventDelete(BaseModel):
    """Confirmation message returned after event has been deleted."""
    message: str


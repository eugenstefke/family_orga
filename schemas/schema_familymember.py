from datetime import date
from pydantic import BaseModel, field_validator, Field, ConfigDict
from typing import Literal, Optional

class FamilyMemberCreate(BaseModel):
    """Required details for creating a new familymember.

    The title and weight -> restricted to 0-250 field must not be empty.
    The birthday must be later than today's date
    The height field is optional, the default value is None and it is restricted to 0–300.
    The type can only be child, adult or pet
    The allergies and clothing size are optional and has default None
    shoe size are optional default is None restricted to 0-70"""

    name: str = Field(min_length=1)
    birthday: date
    height: Optional[int] = Field(default=None, gt=0, lt=300)
    weight: int = Field(gt=0, lt=250)
    type: Literal["child", "adult", "pet"]
    allergies: Optional[str] = None
    clothing_size: Optional[str] = None
    shoe_size: Optional[float] = Field(default=None, gt=0, lt=70)

    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls, value: date) -> date:
        if value > date.today():
            raise ValueError(f"The date of birth cannot be later than today's date {date.today()}")

        return value

class FamilyMemberOut(BaseModel):
    """Data of a familymember, returned after the familymember has been created."""
    id: int
    name: str
    birthday: date
    type: Literal["child", "adult", "pet"]

    model_config = ConfigDict(from_attributes=True)

class FamilyMemberDetail(BaseModel):
    """Details of a familymember."""
    id: int
    name: str
    birthday: date
    height: Optional[int] = None
    weight: int
    type: Literal["child", "adult", "pet"]
    allergies: Optional[str] = None
    clothing_size: Optional[str] = None
    shoe_size: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class FamilyMemberUpdate(BaseModel):
    """Confirmation message returned after a familymember has been updated."""
    message: str

class FamilyMemberDelete(BaseModel):
    """Confirmation message returned after a familymember has been deleted."""
    message: str
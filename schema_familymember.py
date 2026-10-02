from datetime import date
from pydantic import BaseModel, field_validator, Field, ConfigDict
from typing import Literal, Optional

# Request-Modell: Input of registration a familymember
class FamilyMemberCreate(BaseModel):
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

# Output after Creat
class FamilyMemberOut(BaseModel):

    id: int
    name: str
    birthday: date
    type: Literal["child", "adult", "pet"]

    model_config = ConfigDict(from_attributes=True)

#Output for get request
class FamilyMemberDetail(BaseModel):
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

# Output for Update successful
class FamilyMemberUpdate(BaseModel):

    message: str

# Output for Delete
class FamilyMemberDelete(BaseModel):

    message: str
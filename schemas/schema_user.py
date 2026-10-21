from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, Field

SPECIAL_CHARS = set("!§$%&/()=?.,-_#+*")

def check_name(name: str) -> str:
    if not name.strip():
        raise ValueError("The name field must not be left blank")
    return name

def check_password(password: str) -> str:
    if len(password) < 8:
        raise ValueError("The password must be at least 8 characters long")
    if not any(char in SPECIAL_CHARS for char in password):
        raise ValueError("At least one special character is required. Permitted special characters: !§$%&/()=?.,-_#+*")
    return password

class UserCreate(BaseModel):
    """Required details for creating a new user.

    The name, email and password field must not be empty.
    The email field uses pydantic validation – the @ symbol must be present and the domain must be valid
    The password must be at least 8 characters long and must contain special characters"""

    name: str
    email: EmailStr
    password: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        return check_name(value)

    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, value: str) -> str:
        return check_password(value)


class UserLogin(BaseModel):
    """Required details for login"""
    email: EmailStr
    password: str

class UserUpdate(UserCreate):
    """Required details for updating a user: the same fields and rules as when
    creating a user, plus the old password as a security check."""

    old_password: str

class UserDelete(BaseModel):
    """Required field for delete a user """
    password: str

# Response-Modell: Output for Client
class UserOut(BaseModel):
    """Data of a user, returned after the user has been created."""
    id: int
    name: str = Field(validation_alias="user_name") # validation_alias="user_name" pydantic says that the column is called ‘user_name’ and not ‘name’
    email: EmailStr

    model_config = ConfigDict(from_attributes=True) # populate_by_name=True can be passed as an argument if you wish to create a UserOut.name manually (for testing); otherwise, it is not necessary


class UserOutUpdate(BaseModel):
    """Confirmation message returned after a user has been updated."""
    message: str

class UserOutDelete(BaseModel):
    """Confirmation message returned after user has been deleted."""
    message: str
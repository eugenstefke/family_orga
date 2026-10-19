from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, Field

SPECIAL_CHARS = set("!§$%&/()=?.,-_#+*")

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
        if not value.strip():
            raise ValueError("The name field must not be left blank")
        return value

    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("The password must be at least 8 characters long")
        if not any(char in SPECIAL_CHARS for char in value):
            raise ValueError("At least one special character is required. Permitted special characters: !§$%&/()=?.,-_#+*")
        return value


class UserLogin(BaseModel):
    """Required details for login"""
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    """Required details for updating user details.
    The old password is verified as a security measure
    The same validation rules as when creating a new user"""

    name: str
    email: EmailStr
    password: str
    old_password: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("The name field must not be left blank")
        return value

    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("The password must be at least 8 characters long")
        if not any(char in SPECIAL_CHARS for char in value):
            raise ValueError("At least one special character is required. Permitted special characters: !§$%&/()=?.,-_#+*")
        return value

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
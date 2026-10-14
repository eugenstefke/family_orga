from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, Field

SPECIAL_CHARS = set("!§$%&/()=?.,-_#+*")

# Request-Modell: Input of registration
class UserCreate(BaseModel):
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

# Request-Modell: Input of registration
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
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
    password: str

# Response-Modell: Output for Client
class UserOut(BaseModel):
    id: int
    name: str = Field(validation_alias="user_name") # validation_alias="user_name" pydantic says that the column is called ‘user_name’ and not ‘name’
    email: EmailStr

    model_config = ConfigDict(from_attributes=True) # populate_by_name=True can be passed as an argument if you wish to create a UserOut.name manually (for testing); otherwise, it is not necessary


class UserOutUpdate(BaseModel):

    message: str

class UserOutDelete(BaseModel):

    message: str
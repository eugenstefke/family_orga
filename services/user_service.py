from models.models import User
from pwdlib import PasswordHash
from schemas.schema_user import UserCreate, UserLogin, UserUpdate, UserDelete
from repositories.user_repository import IUserRepository

password_hash = PasswordHash.recommended()

class UserService:
    """Business logic for user.
    Works with any repository that implements IUserRepository,
    so the database access can be exchanged without changing the service."""

    def __init__(self, repository: IUserRepository):
        """Initialize the service with the repository used for user data access."""
        self.repository = repository

    def add_new_user(self, user_data: UserCreate):
        """Create user.

        Return (None, new_user) on success.
        Return (message, None) if email already exists"""

        existing = self.repository.get_by_email(email=user_data.email)

        if existing:
            return "This email address is already in use", None

        hashed_password = password_hash.hash(user_data.password)

        new_user = User(
            user_name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password
        )
        self.repository.add_user(new_user=new_user)
        self.repository.commit()
        return None, new_user

    def authenticate_user(self, user_login: UserLogin):
        """Authenticate user by login.

        Return (None, user) on success.
        Return (message, None) if email not correct
        Return (message, None) if password not correct"""

        user = self.repository.get_by_email(email=user_login.email)

        if not user:
            return "Your email address or password is incorrect", None

        password_correct = password_hash.verify(user_login.password, user.hashed_password)

        if not password_correct:
            return "Your email address or password is incorrect", None

        return None, user

    def details_change(self, user_details: UserUpdate, current_user: User):
        """Update the current user details (email, name, password).

        Return (None, None, current_user) on success
        If the old password not correct, return (401, message, None).
        Return (409, message, None) if email already exists"""

        password_correct = password_hash.verify(user_details.old_password, current_user.hashed_password)
        if not password_correct:
            return 401, "Old Password is not correct", None

        existing = self.repository.get_by_email(email=user_details.email)

        if existing and existing.id != current_user.id:
            return 409, "This email address is already in use", None

        current_user.user_name=user_details.name
        current_user.email=user_details.email
        current_user.hashed_password=password_hash.hash(user_details.password)

        self.repository.commit()
        return None, None, current_user

    def delete_user(self, user_password: UserDelete, current_user: User):
        """Delete current user.
        Return (None, user_name) on success
        If the password not correct, return (message, None)."""

        password_correct = password_hash.verify(user_password.password , current_user.hashed_password)
        if not password_correct:
            return "Password is not correct, cannot delete", None

        user_name = current_user.user_name

        self.repository.delete_user(current_user)
        self.repository.commit()

        return None, user_name
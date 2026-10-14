from models.models import User
from pwdlib import PasswordHash
from schema_user import UserCreate, UserLogin, UserUpdate, UserDelete
from repositories.user_repository import IUserRepository

password_hash = PasswordHash.recommended()

class UserService:

    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def add_new_user(self, user_data: UserCreate):

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

        user = self.repository.get_by_email(email=user_login.email)

        if not user:
            return "Your email address or password is incorrect", None

        password_correct = password_hash.verify(user_login.password, user.hashed_password)

        if not password_correct:
            return "Your email address or password is incorrect", None

        return None, user

    def details_change(self, update_user_details: UserUpdate, current_user: User):

        password_correct = password_hash.verify(update_user_details.old_password, current_user.hashed_password)
        if not password_correct:
            return "Old Password is not correct", None

        current_user.user_name=update_user_details.name
        current_user.email=update_user_details.email
        current_user.hashed_password=password_hash.hash(update_user_details.password)

        self.repository.commit()
        return None, current_user

    def delete_user(self, user_password: UserDelete, current_user: User):

        password_correct = password_hash.verify(user_password.password , current_user.hashed_password)
        if not password_correct:
            return "Password is not correct, cannot delete", None

        delete_name = current_user.user_name

        self.repository.delete_user(current_user)
        self.repository.commit()

        return None, delete_name
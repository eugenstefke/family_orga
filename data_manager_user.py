from models import User
from pwdlib import PasswordHash
from schema_user import UserCreate, UserLogin, UserUpdate
from sqlalchemy.orm import Session

password_hash = PasswordHash.recommended()

class DataManagerUser:
    def add_user(self, user_data: UserCreate, db: Session):
        existing = db.query(User).filter_by(email=user_data.email).first()
        if existing:
            return "This email address is already in use", None

        hashed_password = password_hash.hash(user_data.password)

        new_user = User(
            user_name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password
        )
        db.add(new_user)
        db.commit()
        return None, new_user

    def authenticate_user(self, user_login: UserLogin, db: Session):

        user = db.query(User).filter_by(email=user_login.email).first()

        if not user:
            return "Your email address or password is incorrect", None

        password_correct = password_hash.verify(user_login.password, user.hashed_password)

        if not password_correct:
            return "Your email address or password is incorrect", None

        return None, user

    def details_change(self, update_user_details: UserUpdate, current_user: User, db: Session):

        password_correct = password_hash.verify(update_user_details.old_password, current_user.hashed_password)
        if not password_correct:
            return "Old Password is not correct", None

        current_user.user_name=update_user_details.name
        current_user.email=update_user_details.email
        current_user.hashed_password=password_hash.hash(update_user_details.password)

        db.commit()
        return None, current_user

    def delete_user(self, user_password, current_user: User, db: Session):

        password_correct = password_hash.verify(user_password.password , current_user.hashed_password)
        if not password_correct:
            return "Password is not correct, cannot delete", None

        delete_name = current_user.user_name

        db.delete(current_user)
        db.commit()

        return None, delete_name
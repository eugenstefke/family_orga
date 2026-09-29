from models import User, FamilyMember, Event, Doctor, FamilymemberDoctor, FamilymemberEvent
from database import Session
from pwdlib import PasswordHash
from schemas import UserCreate
from sqlalchemy.exc import IntegrityError


session = Session()
password_hash = PasswordHash.recommended()

class DataManager:
    def add_user(self, user_data: UserCreate):
        existing = session.query(User).filter_by(email=user_data.email).first()
        if existing:
            return "This email address is already in use", None

        hashed_password = password_hash.hash(user_data.password)

        new_user = User(
            user_name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password
        )
        session.add(new_user)
        session.commit()
        return None, new_user
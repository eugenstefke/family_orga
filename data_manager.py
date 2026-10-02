from models import User, FamilyMember, Event, Doctor, FamilymemberDoctor, FamilymemberEvent
from database import Session
from pwdlib import PasswordHash

from schema_familymember import FamilyMemberCreate
from schema_user import UserCreate, UserLogin
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

    def authenticate_user(self, user_login: UserLogin):

        user = session.query(User).filter_by(email=user_login.email).first()

        if not user:
            return "E-Mail oder Passwort ist falsch", None

        password_correct = password_hash.verify(user_login.password, user.hashed_password)

        if not password_correct:
            return "E-Mail oder Passwort ist falsch", None

        return None, user

    def add_familymember(self, familymember: FamilyMemberCreate, current_user: User):

        existing = session.query(FamilyMember).filter_by(name=familymember.name, birthday=familymember.birthday, owner_id=current_user.id).first()
        if existing:
            return f"{familymember.name} is already a familymember", None

        new_familymember = FamilyMember(
            name=familymember.name,
            birthday=familymember.birthday,
            height=familymember.height,
            weight=familymember.weight,
            type=familymember.type,
            allergies=familymember.allergies,
            clothing_size=familymember.clothing_size,
            shoe_size=familymember.shoe_size,
            owner_id=current_user.id
        )

        session.add(new_familymember)
        session.commit()
        return None, new_familymember

    def get_familymembers(self, current_user: User):

        familymembers = session.query(FamilyMember).filter_by(owner_id=current_user.id).all()
        return familymembers

    def get_familymember_details(self, current_user: User, familymember_id: int):

        familymember = session.query(FamilyMember).filter_by(owner_id=current_user.id, id=familymember_id).first()

        if not familymember:
            return "Familymember not found", None

        return None, familymember

    def update_familymember_details(self, familymember_id: int, current_user: User, familymember: FamilyMemberCreate):

        update_familymember = session.query(FamilyMember).filter_by(owner_id=current_user.id, id=familymember_id).first()

        if not familymember:
            return "Familymember not found", None

        update_familymember.name = familymember.name
        update_familymember.birthday = familymember.birthday
        update_familymember.height = familymember.height
        update_familymember.weight = familymember.weight
        update_familymember.type = familymember.type
        update_familymember.allergies = familymember.allergies
        update_familymember.clothing_size = familymember.clothing_size
        update_familymember.shoe_size = familymember.shoe_size

        session.commit()
        return None, update_familymember

    def delete_familymember(self, familymember_id: int, current_user: User):

        delete_familymember = session.query(FamilyMember).filter_by(owner_id=current_user.id, id=familymember_id).first()

        name_of_delete_familymember = delete_familymember.name # for save the name of delete familymember

        if not delete_familymember:
            return "Familymember not found", None

        session.delete(delete_familymember)
        session.commit()

        return None, name_of_delete_familymember



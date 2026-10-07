from models import FamilyMember, User
from schema_familymember import FamilyMemberCreate
from sqlalchemy.orm import Session

class DataManagerFamilyMember:

    def add_familymember(self, familymember: FamilyMemberCreate, current_user: User, db: Session):

        existing = db.query(FamilyMember).filter_by(name=familymember.name, birthday=familymember.birthday, owner_id=current_user.id).first()
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

        db.add(new_familymember)
        db.commit()
        return None, new_familymember

    def get_familymembers(self, current_user: User, db: Session):

        familymembers = db.query(FamilyMember).filter_by(owner_id=current_user.id).all()
        return familymembers

    def get_familymember_details(self, current_user: User, familymember_id: int, db: Session):

        familymember = db.query(FamilyMember).filter_by(owner_id=current_user.id, id=familymember_id).first()

        if not familymember:
            return "Familymember not found", None

        return None, familymember

    def update_familymember_details(self, familymember_id: int, current_user: User, familymember_update: FamilyMemberCreate, db: Session):

        familymember = db.query(FamilyMember).filter_by(owner_id=current_user.id, id=familymember_id).first()

        if not familymember:
            return "Familymember not found", None

        familymember.name = familymember_update.name
        familymember.birthday = familymember_update.birthday
        familymember.height = familymember_update.height
        familymember.weight = familymember_update.weight
        familymember.type = familymember_update.type
        familymember.allergies = familymember_update.allergies
        familymember.clothing_size = familymember_update.clothing_size
        familymember.shoe_size = familymember_update.shoe_size

        db.commit()
        return None, familymember

    def delete_familymember(self, familymember_id: int, current_user: User, db: Session):

        familymember_to_delete = db.query(FamilyMember).filter_by(owner_id=current_user.id, id=familymember_id).first()

        if not familymember_to_delete:
            return "Familymember not found", None

        delete_name = familymember_to_delete.name # for save the name of delete familymember

        db.delete(familymember_to_delete)
        db.commit()

        return None, delete_name



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

    def update_familymember_details(self, familymember_id: int, current_user: User, familymember: FamilyMemberCreate, db: Session):

        update_familymember = db.query(FamilyMember).filter_by(owner_id=current_user.id, id=familymember_id).first()

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

        db.commit()
        return None, update_familymember

    def delete_familymember(self, familymember_id: int, current_user: User, db: Session):

        familymember_to_delete = db.query(FamilyMember).filter_by(owner_id=current_user.id, id=familymember_id).first()

        if not familymember_to_delete:
            return "Familymember not found", None

        delete_name = familymember_to_delete.name # for save the name of delete familymember

        db.delete(familymember_to_delete)
        db.commit()

        return None, delete_name



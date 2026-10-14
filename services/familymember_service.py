from models.models import FamilyMember, User
from repositories.familymember_repository import IFamilyMemberRepository
from schemas.schema_familymember import FamilyMemberCreate

class FamilyMemberService:

    def __init__(self, repository: IFamilyMemberRepository):
        self.repository = repository

    def get_familymembers(self, current_user: User):

        familymembers = self.repository.get_all(current_user.id)
        return familymembers

    def get_familymember_details(self, current_user: User, familymember_id: int):

        familymember = self.repository.get_by_id(owner_id=current_user.id, familymember_id=familymember_id)

        if not familymember:
            return "Familymember not found", None

        return None, familymember

    def add_familymember(self, familymember: FamilyMemberCreate, current_user: User):

        existing = self.repository.familymember_existing(familymember_name=familymember.name, familymember_birthday=familymember.birthday, owner_id=current_user.id)

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

        self.repository.add_familymember(new_familymember=new_familymember)
        self.repository.commit()
        return None, new_familymember

    def update_familymember_details(self, familymember_id: int, current_user: User, familymember_update: FamilyMemberCreate):

        familymember = self.repository.get_by_id(owner_id=current_user.id, familymember_id=familymember_id)

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

        self.repository.commit()
        return None, familymember

    def delete_familymember(self, familymember_id: int, current_user: User):

        familymember_to_delete = self.repository.get_by_id(owner_id=current_user.id, familymember_id=familymember_id)

        if not familymember_to_delete:
            return "Familymember not found", None

        delete_name = familymember_to_delete.name  # for save the name of delete familymember

        self.repository.delete_familymember(familymember=familymember_to_delete)
        self.repository.commit()

        return None, delete_name
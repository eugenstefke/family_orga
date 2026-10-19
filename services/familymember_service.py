from models.models import FamilyMember, User
from repositories.familymember_repository import IFamilyMemberRepository
from schemas.schema_familymember import FamilyMemberCreate

class FamilyMemberService:
    """Business logic for familymember.
    Works with any repository that implements IFamilyMemberRepository,
    so the database access can be exchanged without changing the service."""

    def __init__(self, repository: IFamilyMemberRepository):
        """Initialize the service with the repository used for familymember data access."""
        self.repository = repository

    def get_familymembers(self, current_user: User):
        """Returns all familymembers of the given user as a list"""
        familymembers = self.repository.get_all(current_user.id)
        return familymembers

    def get_familymember_details(self, current_user: User, familymember_id: int):
        """Return the familymember with the given ID if it belongs to the user.
        Return (None,familymember) on success
        If the familymember not found, return (“Familymember not found”, None)."""

        familymember = self.repository.get_by_id(owner_id=current_user.id, familymember_id=familymember_id)

        if not familymember:
            return "Familymember not found", None

        return None, familymember

    def add_familymember(self, familymember: FamilyMemberCreate, current_user: User):
        """Create familymember for the given user.

        Return (None, new_familymember) on success.
        Return (message, None) if familymember already exist"""

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
        """Update the familymember with the given ID and user.

        Return (None, familymember) on success
        If the familymember not found, return (“familymember not found”, None)."""

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
        """Delete familymember with the given familymember id and user.
        Return (None, familymember_name) on success
        If the familymember not found, return (“familymember not found”, None)."""

        familymember_to_delete = self.repository.get_by_id(owner_id=current_user.id, familymember_id=familymember_id)

        if not familymember_to_delete:
            return "Familymember not found", None

        familymember_name = familymember_to_delete.name  # keep the name for the response, the familymember is deleted afterwards

        self.repository.delete_familymember(familymember=familymember_to_delete)
        self.repository.commit()

        return None, familymember_name
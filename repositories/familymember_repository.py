from abc import ABC, abstractmethod

class IFamilyMemberRepository(ABC):
    """Parent class that defines the methods"""

    @abstractmethod
    def get_all(self, owner_id):
        pass

    @abstractmethod
    def get_by_id(self, owner_id, familymember_id):
        pass

    @abstractmethod
    def familymember_existing(self, familymember_name, familymember_birthday, owner_id):
        pass

    @abstractmethod
    def add_familymember(self, new_familymember):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def delete_familymember(self, familymember):
        pass
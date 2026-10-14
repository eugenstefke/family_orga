from abc import ABC, abstractmethod

class IUserRepository(ABC):

    @abstractmethod
    def get_by_email(self, email):
        pass

    @abstractmethod
    def add_user(self, new_user):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def delete_user(self, user):
        pass
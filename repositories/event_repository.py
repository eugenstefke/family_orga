from abc import ABC, abstractmethod

class IEventRepository(ABC):
    """Parent class that defines the methods"""

    @abstractmethod
    def get_by_id(self, owner_id, event_id):
        pass

    @abstractmethod
    def get_all(self, owner_id):
        pass

    @abstractmethod
    def add_event(self, new_event):
        pass

    @abstractmethod
    def flush(self):
        pass

    @abstractmethod
    def validation(self, event_details, current_user):
        pass

    @abstractmethod
    def add_linking(self, familymember_id, event_id):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def delete_linking(self, event_id):
        pass

    @abstractmethod
    def delete_event(self, event):
        pass
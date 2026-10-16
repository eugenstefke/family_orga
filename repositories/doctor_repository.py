from abc import ABC, abstractmethod

class IDoctorRepository(ABC):
    """Parent class that defines the methods"""

    @abstractmethod
    def add_doctor(self, new_doctor):
        pass

    @abstractmethod
    def add_linking(self, familymember_id, doctor_id):
        pass

    @abstractmethod
    def flush(self):
        pass

    @abstractmethod
    def validation(self, doctor_details, current_user):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def get_by_id(self, owner_id, doctor_id):
        pass

    @abstractmethod
    def get_all(self, owner_id):
        pass

    @abstractmethod
    def delete_doctor(self, owner_id, doctor_id):
        pass

    @abstractmethod
    def delete_linking(self, doctor_id):
        pass
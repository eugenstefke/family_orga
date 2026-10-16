from repositories.user_repository import IUserRepository
from sqlalchemy.orm import Session
from models.models import User


class UserRepositorySqlalchemy(IUserRepository):
    """Child class of IUserRepository that implements its methods"""

    def  __init__ (self, session: Session):
        """Store the database session that is shared across the request"""
        self.db = session

    def get_by_email(self, email):
        """Returns user based on their email"""
        return self.db.query(User).filter_by(email=email).first()

    def add_user(self, new_user):
        """Stage a new user for insertion"""
        self.db.add(new_user)

    def commit(self):
        """Make all pending changes permanent"""
        self.db.commit()

    def delete_user(self, user):
        """Deletes a user"""
        self.db.delete(user)
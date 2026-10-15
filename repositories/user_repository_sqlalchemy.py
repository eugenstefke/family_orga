from repositories.user_repository import IUserRepository
from sqlalchemy.orm import Session
from models.models import User


class UserRepositorySqlalchemy(IUserRepository):

    def  __init__ (self, session: Session):
        self.db = session

    def get_by_email(self, email):
        return self.db.query(User).filter_by(email=email).first()

    def add_user(self, new_user):
        self.db.add(new_user)

    def commit(self):
        self.db.commit()

    def delete_user(self, user):
        self.db.delete(user)
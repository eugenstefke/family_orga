from schema_user import UserCreate, UserOut, UserLogin, UserOutUpdate, UserUpdate, UserOutDelete, UserDelete
from sqlalchemy.orm import Session
from fastapi import  HTTPException, Depends, APIRouter
from database import get_db
from auth.auth_users import create_access_token, get_current_user
from models.models import User
from repositories.user_repository_sqlalchemy import UserRepositorySqlalchemy
from services.user_service import UserService

router = APIRouter()

##### Neu #####

@router.post("/user/registration", response_model=UserOut) #response_model=UserOut tells FastAPI to format the response as in UserOut before sending it to the client
def create_user(user: UserCreate, db: Session = Depends(get_db)): #user: UserCreate checks the client’s input; if the input does not match the UserCreate schema, it is automatically rejected; if everything matches, the user is passed as an argument to the UserCreate object
    repository = UserRepositorySqlalchemy(session=db)
    service = UserService(repository=repository)
    message, new_user = service.add_new_user(user)

    if message:
        raise HTTPException(status_code=400, detail=message)
    return new_user

@router.post("/user/login")
def user_login(user_login: UserLogin, db: Session = Depends(get_db)):
    repository = UserRepositorySqlalchemy(session=db)
    service = UserService(repository=repository)
    message, user = service.authenticate_user(user_login)
    if message:
        raise HTTPException(status_code=400, detail=message)

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/user/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/user/details/change", response_model=UserOutUpdate)
def user_details_change(update_user_details: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = UserRepositorySqlalchemy(session=db)
    service = UserService(repository=repository)
    message, user_update = service.details_change(update_user_details, current_user)

    if message:
        raise HTTPException(status_code=404, detail=message)
    return UserOutUpdate(message=f"Details update of User {user_update.user_name} successful")

@router.delete("/user/delete", response_model=UserOutDelete)
def user_delete(password_for_delete: UserDelete, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = UserRepositorySqlalchemy(session=db)
    service = UserService(repository=repository)
    message, delete_user = service.delete_user(password_for_delete, current_user)

    if message:
        raise HTTPException(status_code=404, detail=message)
    return UserOutDelete(message=f"User {delete_user} delete successful")
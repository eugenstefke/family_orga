from fastapi import FastAPI, HTTPException, Depends
from schema_user import UserCreate, UserOut, UserLogin
from schema_familymember import FamilyMemberCreate, FamilyMemberOut, FamilyMemberDetail, FamilyMemberUpdate, FamilyMemberDelete
from data_manager import DataManager
from models import User
import uvicorn
from auth.auth_users import create_access_token, get_current_user

app = FastAPI()

@app.post("/user/registration", response_model=UserOut) #response_model=UserOut tells FastAPI to format the response as in UserOut before sending it to the client
def create_user(user: UserCreate): #user: UserCreate checks the client’s input; if the input does not match the UserCreate schema, it is automatically rejected; if everything matches, the user is passed as an argument to the UserCreate object
    message, new_user = DataManager().add_user(user)
    if message:
        raise HTTPException(status_code=400, detail=message)
    return new_user

@app.post("/user/login")
def user_login(user_login: UserLogin):
    message, user = DataManager().authenticate_user(user_login)
    if message:
        raise HTTPException(status_code=400, detail=message)

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/user/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/familymembers/get", response_model=list[FamilyMemberOut])
def read_familymembers(current_user: User = Depends(get_current_user)):
    familymembers = DataManager().get_familymembers(current_user)

    return familymembers

@app.get("/familymember/{familymember_id}", response_model=FamilyMemberDetail)
def read_familymember_details(familymember_id: int, current_user: User = Depends(get_current_user)):
    message, familymember_details = DataManager().get_familymember_details(current_user, familymember_id)
    if message:
        raise HTTPException(status_code=404, detail=message)
    return familymember_details

@app.post("/familymember/create", response_model=FamilyMemberOut)
def create_familymember(familymember: FamilyMemberCreate, current_user: User = Depends(get_current_user)):
    message, new_familymember = DataManager().add_familymember(familymember, current_user)
    if message:
        raise HTTPException(status_code=400, detail=message)
    return new_familymember

@app.put("/familymember/{familymember_id}", response_model=FamilyMemberUpdate)
def update_familymember(familymember_id : int, familymember: FamilyMemberCreate, current_user: User = Depends(get_current_user)):
    message, familymember_update = DataManager().update_familymember_details(familymember_id, current_user, familymember)
    if message:
        raise HTTPException(status_code=400, detail=message)
    return FamilyMemberUpdate(message=f"Details update of Familymember {familymember_update.name} successful")

@app.delete("/familymember/{familymember_id}", response_model=FamilyMemberDelete)
def delete_familymember(familymember_id : int, current_user: User = Depends(get_current_user)):
    message, familymember_delete = DataManager().delete_familymember(familymember_id, current_user)

    if message:
        raise HTTPException(status_code=400, detail=message)

    return FamilyMemberDelete(message=f"{familymember_delete} is not more in your list")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)


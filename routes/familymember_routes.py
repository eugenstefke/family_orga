from models.models import User
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from schema_familymember import FamilyMemberCreate, FamilyMemberOut, FamilyMemberDetail, FamilyMemberUpdate, FamilyMemberDelete
from auth.auth_users import get_current_user
from datamanager_familymember import DataManagerFamilyMember
from database import get_db
app = FastAPI()

@app.get("/get/all/familymembers", response_model=list[FamilyMemberOut])
def read_familymembers(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    familymembers = DataManagerFamilyMember().get_familymembers(current_user, db)

    return familymembers

@app.get("/familymember/{familymember_id}", response_model=FamilyMemberDetail)
def read_familymember_details(familymember_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, familymember_details = DataManagerFamilyMember().get_familymember_details(current_user, familymember_id, db)
    if message:
        raise HTTPException(status_code=404, detail=message)
    return familymember_details

@app.post("/familymember/create", response_model=FamilyMemberOut)
def create_familymember(familymember: FamilyMemberCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, new_familymember = DataManagerFamilyMember().add_familymember(familymember, current_user, db)
    if message:
        raise HTTPException(status_code=400, detail=message)
    return new_familymember

@app.put("/familymember/{familymember_id}", response_model=FamilyMemberUpdate)
def update_familymember(familymember_id : int, familymember: FamilyMemberCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, familymember = DataManagerFamilyMember().update_familymember_details(familymember_id, current_user, familymember, db)
    if message:
        raise HTTPException(status_code=400, detail=message)
    return FamilyMemberUpdate(message=f"Details update of Familymember {familymember.name} successful")

@app.delete("/familymember/{familymember_id}", response_model=FamilyMemberDelete)
def delete_familymember(familymember_id : int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, familymember = DataManagerFamilyMember().delete_familymember(familymember_id, current_user, db)

    if message:
        raise HTTPException(status_code=400, detail=message)

    return FamilyMemberDelete(message=f"{familymember} is no longer in your list")

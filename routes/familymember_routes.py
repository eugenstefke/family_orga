from models.models import User
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from schemas.schema_familymember import FamilyMemberCreate, FamilyMemberOut, FamilyMemberDetail, FamilyMemberUpdate, FamilyMemberDelete
from auth.auth_users import get_current_user
from data.database import get_db
from repositories.familymember_repository_sqlalchemy import FamilyMemberRepositorySqlalchemy
from services.familymember_service import FamilyMemberService

router = APIRouter()

@router.get("/get/all/familymembers", response_model=list[FamilyMemberOut])
def read_familymembers(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = FamilyMemberRepositorySqlalchemy(session=db)
    service = FamilyMemberService(repository=repository)
    familymembers = service.get_familymembers(current_user)

    return familymembers

@router.get("/familymember/{familymember_id}", response_model=FamilyMemberDetail)
def read_familymember_details(familymember_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = FamilyMemberRepositorySqlalchemy(session=db)
    service = FamilyMemberService(repository=repository)
    message, familymember_details = service.get_familymember_details(current_user, familymember_id)

    if message:
        raise HTTPException(status_code=404, detail=message)
    return familymember_details

@router.post("/familymember/create", response_model=FamilyMemberOut)
def create_familymember(familymember: FamilyMemberCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = FamilyMemberRepositorySqlalchemy(session=db)
    service = FamilyMemberService(repository=repository)
    message, new_familymember = service.add_familymember(familymember, current_user)

    if message:
        raise HTTPException(status_code=400, detail=message)
    return new_familymember

@router.put("/familymember/{familymember_id}", response_model=FamilyMemberUpdate)
def update_familymember(familymember_id : int, familymember: FamilyMemberCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = FamilyMemberRepositorySqlalchemy(session=db)
    service = FamilyMemberService(repository=repository)
    message, familymember = service.update_familymember_details(familymember_id, current_user, familymember)

    if message:
        raise HTTPException(status_code=400, detail=message)
    return FamilyMemberUpdate(message=f"Details update of Familymember {familymember.name} successful")

@router.delete("/familymember/{familymember_id}", response_model=FamilyMemberDelete)
def delete_familymember(familymember_id : int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = FamilyMemberRepositorySqlalchemy(session=db)
    service = FamilyMemberService(repository=repository)
    message, familymember = service.delete_familymember(familymember_id, current_user)

    if message:
        raise HTTPException(status_code=400, detail=message)

    return FamilyMemberDelete(message=f"{familymember} is no longer in your list")
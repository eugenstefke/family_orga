from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, APIRouter
from schemas.schema_doctor import DoctorCreate, DoctorOut, DoctorDetail, AllDoctorsOut, DoctorUpdateOut, DoctorDeleteOut
from models.models import User
from data.database import get_db
from auth.auth_users import get_current_user
from repositories.doctor_repository_sqlalchemy import DoctorRepositorySqlalchemy
from services.doctor_service import DoctorService
router = APIRouter()

@router.post("/doctor/add", response_model=DoctorOut)
def add_doctor(doctor_details: DoctorCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Add a new doctor for the logged-in user and link them to the given family members id.
    Returns 400 if one of the family member IDs is invalid or belongs to another user."""
    repository = DoctorRepositorySqlalchemy(session=db)
    service = DoctorService(repository=repository)
    message, doctor = service.add_new_doctor(doctor_details, current_user)

    if message:
        raise HTTPException(status_code=400, detail=message)

    return doctor

@router.get("/doctor/{doctor_id}", response_model=DoctorDetail)
def read_doctor_details(doctor_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Return the details of the doctor with the given ID
    Returns 404 if doctor not found with given id, linked to the current user ID"""
    repository = DoctorRepositorySqlalchemy(session=db)
    service = DoctorService(repository=repository)
    message, doctor_details = service.get_doctor_details(doctor_id, current_user)

    if message:
        raise HTTPException(status_code=404, detail=message)
    return doctor_details

@router.get("/get/all/doctors", response_model=list[AllDoctorsOut])
def read_doctors(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Return all doctors of the logged-in user
    Return a empty list if no doctors in the current user list"""
    repository = DoctorRepositorySqlalchemy(session=db)
    service = DoctorService(repository=repository)
    doctors = service.get_doctors(current_user)
    return doctors

@router.put("/doctor/{doctor_id}", response_model=DoctorUpdateOut)
def update_doctor(doctor_id: int, doctor: DoctorCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update the details of the doctor with the given ID

    Returns 404 if the doctor does not exist.
    Returns 400 if one of the given family member IDs is invalid."""
    repository = DoctorRepositorySqlalchemy(session=db)
    service = DoctorService(repository=repository)
    status_code, message, doctor = service.update_doctor(doctor_id, current_user, doctor)

    if message:
        raise HTTPException(status_code=status_code, detail=message)
    return DoctorUpdateOut(message=f"Details change of Doctor {doctor.name} was successfull")

@router.delete("/doctor/{doctor_id}", response_model=DoctorDeleteOut)
def delete_doctor(doctor_id: int, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """Delete the doctor with the given ID
    Returns 404 if doctor not found"""
    repository = DoctorRepositorySqlalchemy(session=db)
    service = DoctorService(repository=repository)
    message, doctor = service.delete_doctor(doctor_id, current_user)

    if message:
        raise HTTPException(status_code=404, detail=message)

    return DoctorDeleteOut(message=f"{doctor} is no longer in your list")



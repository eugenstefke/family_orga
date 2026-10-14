from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from schema_doctor import DoctorCreate, DoctorOut, DoctorDetail, AllDoctorsOut, DoctorUpdate, DoctorDelete
from models.models import User
from database import get_db
from auth.auth_users import get_current_user
from repositories.doctor_repository_sqlalchemy import DoctorRepositorySqlalchemy
from services.doctor_service import DoctorServie

router = APIRouter()

######### Neu ##########

@router.post("/doctor/add", response_model=DoctorOut)
def add_doctor(doctor_details: DoctorCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = DoctorRepositorySqlalchemy(session=db)
    service = DoctorServie(repository=repository)
    message, doctor = service.add_new_doctor(doctor_details, current_user)

    if message:
        raise HTTPException(status_code=400, detail=message)

    return doctor

@router.get("/doctor/{doctor_id}", response_model=DoctorDetail)
def read_doctor_details(doctor_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = DoctorRepositorySqlalchemy(session=db)
    service = DoctorServie(repository=repository)
    message, doctor_details = service.get_doctor_details(doctor_id, current_user)

    if message:
        raise HTTPException(status_code=404, detail=message)
    return doctor_details

@router.get("/get/all/doctors", response_model=list[AllDoctorsOut])
def read_doctors(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = DoctorRepositorySqlalchemy(session=db)
    service = DoctorServie(repository=repository)
    doctors = service.get_doctors(current_user)
    return doctors

@router.put("/doctor/{doctor_id}", response_model=DoctorUpdate)
def update_doctor(doctor_id: int, doctor: DoctorCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = DoctorRepositorySqlalchemy(session=db)
    service = DoctorServie(repository=repository)
    message, doctor = service.update_doctor(doctor_id, current_user, doctor)

    if message:
        raise HTTPException(status_code=400, detail=message)
    return DoctorUpdate(message=f"Details change of Doctor {doctor.name} was successfull")

@router.delete("/doctor/{doctor_id}", response_model=DoctorDelete)
def delete_doctor(doctor_id: int, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    repository = DoctorRepositorySqlalchemy(session=db)
    service = DoctorServie(repository=repository)
    message, doctor = service.delete_doctor(doctor_id, current_user)

    if message:
        raise HTTPException(status_code=400, detail=message)

    return DoctorDelete(message=f"{doctor} is no longer in your list")



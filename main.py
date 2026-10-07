from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from schema_user import UserCreate, UserOut, UserLogin, UserOutUpdate, UserUpdate, UserOutDelete, UserDelete
from schema_familymember import FamilyMemberCreate, FamilyMemberOut, FamilyMemberDetail, FamilyMemberUpdate, FamilyMemberDelete
from schema_event import EventCreate, EventOut, EventDetail, AllEventsOut, EventUpdate, EventDelete
from datamanager_familymember import DataManagerFamilyMember
from datamanager_user import DataManagerUser
from datamanager_event import DataManagerEvent
from datamanager_doctor import DataManagerDoctor
from schema_doctor import DoctorCreate, DoctorOut, DoctorDetail, AllDoctorsOut, DoctorUpdate, DoctorDelete
from models import User
from database import get_db
import uvicorn
from auth.auth_users import create_access_token, get_current_user
app = FastAPI()

@app.post("/user/registration", response_model=UserOut) #response_model=UserOut tells FastAPI to format the response as in UserOut before sending it to the client
def create_user(user: UserCreate, db: Session = Depends(get_db)): #user: UserCreate checks the client’s input; if the input does not match the UserCreate schema, it is automatically rejected; if everything matches, the user is passed as an argument to the UserCreate object
    message, new_user = DataManagerUser().add_user(user, db)
    if message:
        raise HTTPException(status_code=400, detail=message)
    return new_user

@app.post("/user/login")
def user_login(user_login: UserLogin, db: Session = Depends(get_db)):
    message, user = DataManagerUser().authenticate_user(user_login, db)
    if message:
        raise HTTPException(status_code=400, detail=message)

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/user/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@app.put("/user/details/change", response_model=UserOutUpdate)
def user_details_change(update_user_details: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, user_update = DataManagerUser().details_change(update_user_details, current_user, db)
    if message:
        raise HTTPException(status_code=404, detail=message)
    return UserOutUpdate(message=f"Details update of User {user_update.user_name} successful")

@app.delete("/user/delete", response_model=UserOutDelete)
def user_delete(password_for_delete: UserDelete, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, delete_user = DataManagerUser().delete_user(password_for_delete, current_user, db)
    if message:
        raise HTTPException(status_code=404, detail=message)
    return UserOutDelete(message=f"User {delete_user} delete successful")

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

@app.get("/event/{event_id}", response_model=EventDetail)
def read_event_details(event_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, event_details = DataManagerEvent().get_event_details(event_id, current_user, db)
    if message:
        raise HTTPException(status_code=404, detail=message)
    return event_details

@app.get("/get/all/events", response_model=list[AllEventsOut])
def read_events(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    events = DataManagerEvent().get_events(current_user, db)
    return events

@app.post("/event/create", response_model=EventOut)
def create_event(event_details: EventCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, event = DataManagerEvent().add_event(event_details, current_user, db)
    if message:
        raise HTTPException(status_code=400, detail=message)

    return EventOut(message=f"{event.title} on {event.date_time} added")

@app.put("/event/{event_id}", response_model=EventUpdate)
def update_event(event_id: int, event: EventCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, event = DataManagerEvent().update_event(event_id, current_user, event, db)
    if message:
        raise HTTPException(status_code=400, detail=message)
    return EventUpdate(message=f"The changes made for the {event.title} event were successfull")

@app.delete("/event/{event_id}", response_model=EventDelete)
def delete_event(event_id: int, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    message, event = DataManagerEvent().delete_event(event_id, current_user, db)

    if message:
        raise HTTPException(status_code=400, detail=message)

    return EventDelete(message=f"{event} is no longer in your list")

@app.get("/doctor/{doctor_id}", response_model=DoctorDetail)
def read_doctor_details(doctor_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, doctor_details = DataManagerDoctor().get_doctor_details(doctor_id, current_user, db)
    if message:
        raise HTTPException(status_code=404, detail=message)
    return doctor_details

@app.get("/get/all/doctors", response_model=list[AllDoctorsOut])
def read_doctors(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    doctors = DataManagerDoctor().get_doctors(current_user, db)
    return doctors

@app.post("/doctor/add", response_model=DoctorOut)
def add_doctor(doctor_details: DoctorCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, doctor = DataManagerDoctor().add_new_doctor(doctor_details, current_user, db)
    if message:
        raise HTTPException(status_code=400, detail=message)

    return doctor

@app.put("/doctor/{doctor_id}", response_model=DoctorUpdate)
def update_doctor(doctor_id: int, doctor: DoctorCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message, doctor = DataManagerDoctor().update_doctor(doctor_id, current_user, doctor, db)
    if message:
        raise HTTPException(status_code=400, detail=message)
    return DoctorUpdate(message=f"Details change of Doctor {doctor.name} was successfull")

@app.delete("/doctor/{doctor_id}", response_model=DoctorDelete)
def delete_doctor(doctor_id: int, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    message, doctor = DataManagerDoctor().delete_doctor(doctor_id, current_user, db)

    if message:
        raise HTTPException(status_code=400, detail=message)

    return DoctorDelete(message=f"{doctor} is no longer in your list")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)


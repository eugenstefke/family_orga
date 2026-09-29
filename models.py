from sqlalchemy import Column, Integer, String, Date, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
import enum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

class FamilyMemberType(str, enum.Enum):   # Inherits from string and enum.Enum ensures that the type in familymembers is one of child, adult, pet

    child = "child"
    adult = "adult"
    pet = "pet"

class FamilyMember(Base):
    __tablename__ = "familymembers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    height = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=False)
    type = Column(SQLEnum(FamilyMemberType), nullable=False)  # child, adult, pet
    allergies = Column(String)
    clothing_size = Column(String, nullable=True)
    shoe_size = Column(Float, nullable=True)
    events = relationship("Event", secondary="familymember_events", back_populates="family_members")
    doctors = relationship("Doctor", secondary="familymember_doctors", back_populates="family_members")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    category = Column(String)
    family_members = relationship("FamilyMember", secondary="familymember_events", back_populates="events")

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    field_of_study = Column(String, nullable=False)
    contact_details = Column(String, nullable=False)
    family_members = relationship("FamilyMember", secondary="familymember_doctors", back_populates="doctors")

class FamilymemberEvent(Base):
    __tablename__ = "familymember_events"

    familymember_id = Column(Integer, ForeignKey('familymembers.id', ondelete='CASCADE'), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id', ondelete='CASCADE'), primary_key=True)

class FamilymemberDoctor(Base):
    __tablename__ = "familymember_doctors"

    familymember_id = Column(Integer, ForeignKey('familymembers.id', ondelete='CASCADE'), primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id', ondelete='CASCADE'), primary_key=True)
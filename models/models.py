from sqlalchemy import Column, Integer, String, Date, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from data.database import Base
import enum

class User(Base):
    """Represents the users table
    with columns for the user’s ID, username, email address and hashed password

    The table has a relationship with the family members, events and doctors tables
    such that, if a user is deleted, their entries are also deleted."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    # cascade="all, delete-orphan" -> If the user is deleted, the referenced FamilyMember objects are also deleted, rather than simply setting their foreign key to NULL (set to Null = default behaviour).”
    # passive_deletes=True -> DB handles the deletion itself (thanks to `ondelete=‘CASCADE’` in the Event/Doctor model)
    family_members = relationship("FamilyMember", back_populates="owner", cascade="all, delete-orphan", passive_deletes=True)
    events = relationship("Event", back_populates="owner", cascade="all, delete-orphan", passive_deletes=True)
    doctors = relationship("Doctor", back_populates="owner", cascade="all, delete-orphan", passive_deletes=True)

class FamilyMemberType(str, enum.Enum):
    """Inherits from string and enum.Enum ensures that the type in familymembers is one of child, adult, pet"""

    child = "child"
    adult = "adult"
    pet = "pet"

class FamilyMember(Base):
    """Represents the familymember table
    with columns for the familymember ID, familymember name, birthday, height, weight, type, allergies, clothing size, shoe size and owner id (user id)

    The table has a relationship with the user, events and doctors tables"""
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
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="family_members")
    events = relationship("Event", secondary="familymember_events", back_populates="family_members")
    doctors = relationship("Doctor", secondary="familymember_doctors", back_populates="family_members")

class Event(Base):
    """Represents the event table
    with columns for the event ID, title, data_time, location, category, and owner id (user id)

    The table has a relationship with the user, familymember tables"""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    category = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="events")
    family_members = relationship("FamilyMember", secondary="familymember_events", back_populates="events")

class Doctor(Base):
    """Represents the doctor table
    with columns for the doctor ID, doctor name, field of study, contact details, and owner id (user id)

    The table has a relationship with the user, familymember tables"""
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    field_of_study = Column(String, nullable=False)
    contact_details = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="doctors")
    family_members = relationship("FamilyMember", secondary="familymember_doctors", back_populates="doctors")

class FamilymemberEvent(Base):
    """Represents the FamilymemberEvent table
    with columns for the familymember ID, event id"""

    __tablename__ = "familymember_events"

    familymember_id = Column(Integer, ForeignKey('familymembers.id', ondelete='CASCADE'), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id', ondelete='CASCADE'), primary_key=True)

class FamilymemberDoctor(Base):
    """Represents the FamilymemberEvent table
    with columns for the familymember ID, event id"""

    __tablename__ = "familymember_doctors"

    familymember_id = Column(Integer, ForeignKey('familymembers.id', ondelete='CASCADE'), primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id', ondelete='CASCADE'), primary_key=True)
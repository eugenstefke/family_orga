from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a database connection
engine = create_engine(DATABASE_URL)

# Create a session factory
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for the table class(es)
class Base (DeclarativeBase):
    pass

def get_db():
    """Provide a database session per request and close it afterwards."""
    db = Session()
    try:
        yield db # the session passes on everything that uses Depends(get_db)
    finally: # closes the session, regardless of whether it was successful or failed
        db.close()
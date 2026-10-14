from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Datenbankverbindung erstellen
engine = create_engine(DATABASE_URL)

# Session-Factory erstellen
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Basisklasse für die Tabellenklasse(n) definieren
class Base (DeclarativeBase):
    pass

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
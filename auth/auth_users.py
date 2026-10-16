import os
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from data.database import get_db
from sqlalchemy.orm import Session
from models.models import User

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

# Creates a simple "Authorize" dialogue box with a token field in /docs
security = HTTPBearer()


def create_access_token(user_id: int) -> str:
    """
    Create a signed JWT access token for the given user ID.

    The token's payload contains the user ID (as 'sub') and an expiration
    timestamp (as 'exp'), set to the configured number of minutes from now.

    returns the access token as combination from payload + SECRET_KEY + HS256 Algorithmus
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    """
    Through Depends(security)  FastAPI automatically calls security to read the Authorization-Header. It checks whether the Bearer format is being used.
    FastAPI automatically initiates a new database session via Depends(get_db)

    The encrypted token is decoded using credentials.credentials, whereby the token is extracted as a plain string.

    payload verifies the received token against the SECRET_KEY; an automatic check is carried out to ensure that the token is still within its validity period.
    user_id = payload.get(‘sub’) retrieves the user_id from the token; if user_id is None, a credentials_exception is raised. Error 401 UNAUTHORISED

    jwt.PyJWTError catches any errors that may occur and, for security reasons, consistently returns a 401 UNAUTHORISED status.

    The actual user is then retrieved from the database, following a check to ensure that they still exist.

    return the current user object
    """

    token = credentials.credentials

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token",)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.query(User).get(int(user_id))
    if user is None:
        raise credentials_exception

    return user
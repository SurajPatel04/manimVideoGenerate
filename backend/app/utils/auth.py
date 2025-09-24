from jose import (
    JWTError, 
    jwt
)
from datetime import (
    datetime, 
    timedelta, 
    timezone
)
from fastapi import (
    status, 
    HTTPException,
    Request
)
from app.schema.UserSchema import TokenData
from app.config import Config
import logging

ACCESS_TOKEN_SECRET_KEY = Config.ACCESS_TOKEN_SECRET_KEY
REFRESH_TOKEN_SECRET_KEY = Config.REFRESH_TOKEN_SECRET_KEY
ALGORITHM = Config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_TIME
REFRESH_TOKEN_EXPIRE_DAYS = Config.REFRESH_TOKEN_EXPIRE_DAYS


def createAccessToken(data: dict):
    toEncode=data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    toEncode.update({"exp":expire})
    encodedJWT=jwt.encode(toEncode, ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encodedJWT

def createRefreshToken(data: dict):
    toEncode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
    toEncode.update({"exp":expire})
    encodedJWT=jwt.encode(toEncode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encodedJWT

def verifyAccessToken(token: str, credentialException):
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentialException
        tokenData = TokenData(id=user_id)
    except JWTError as e:
        # Log the underlying JWT error for debugging (do not log the token itself)
        logging.getLogger(__name__).warning("verifyAccessToken failed: %s", repr(e))
        raise credentialException
    
    return tokenData

def verifyRefreshToken(token: str):
    """Verifies the refresh token. Raises exception if invalid."""
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credential_exception
        token_data = TokenData(id=user_id)
    except JWTError as e:
        logging.getLogger(__name__).warning("verifyRefreshToken failed: %s", repr(e))
        raise credential_exception
    
    return token_data


def getCurrentUser(request: Request):
    credentialException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate access token",
        headers={"WWW-authenticate": "Bearer"},
    )

    cookie_token = request.cookies.get("accessToken")
    if not cookie_token:
        logging.getLogger(__name__).warning("accessToken cookie not found on request")
        raise credentialException

    try:
        return verifyAccessToken(cookie_token, credentialException)
    except Exception as e:
        logging.getLogger(__name__).warning("Cookie accessToken verification failed: %s", repr(e))
        raise credentialException

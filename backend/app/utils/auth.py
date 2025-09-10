from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from dotenv import load_dotenv
from app.schema.UserSchema import TokenData
import os

load_dotenv()

ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY", "default_access_secret")
REFRESH_TOKEN_SECRET_KEY = os.getenv("REFRESH_TOKEN_SECRET_KEY", "default_refresh_secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_TIME", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

oauth2Schema = OAuth2PasswordBearer(tokenUrl="login")

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
    except JWTError:
        raise credentialException
    
    return tokenData

def verifyRefreshToken(token: str, credential_exception):
    """Verifies the refresh token. Raises exception if invalid."""
    try:
        # CRITICAL FIX: Use the REFRESH_TOKEN_SECRET_KEY to decode the refresh token.
        # Your original code was using the access token key, which would always fail.
        payload = jwt.decode(token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credential_exception
        token_data = TokenData(id=user_id)
    except JWTError:
        raise credential_exception
    
    return token_data


def getCurrentUser(token: str=Depends(oauth2Schema)):
    credentialException=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="could not verfify",
        headers={"WWW-authenticate":"Bearer"}
    )
    return verifyAccessToken(token, credentialException)

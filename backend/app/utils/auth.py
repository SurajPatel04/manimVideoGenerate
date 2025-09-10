from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from dotenv import load_dotenv
from app.schema.UserSchema import Token
import os
load_dotenv()

oauth2Schema = OAuth2PasswordBearer(tokenUrl="login")

def createAccessToken(data: dict):
    toEncode=data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_TIME")))
    toEncode.update({"exp":expire})
    encodedJWT=jwt.encode(toEncode, os.getenv("ACCESS_TOKEN_SECRET_KEY"), os.getenv("ALGORITHM"))
    return encodedJWT

def createRefreshToken(data: dict):
    toEncode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_TIME")))
    toEncode.update({"exp":expire})
    encodedJWT=jwt.encode(toEncode, os.getenv("REFRESH_TOKEN_SECRET_KEY"), os.getenv("ALGORITHM"))
    return encodedJWT

def verifyAccessToken(token: str, credentialException):
    try:
        payload = jwt.decode(token, os.getenv("ACCESS_TOKEN_SECRET_KEY"), algorithms=os.getenv("ALGORITHM"))
        id: str = payload.get("user_id")
        if id is None:
            raise credentialException
        tokenData = Token(id=str(id))
    except JWTError:
        raise credentialException
    
    return tokenData

def getCurrentUser(token: str=Depends(oauth2Schema)):
    credentialException=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could now verfify", headers={"WWW-authenticate":"Bearer"})
    return verifyAccessToken(token, credentialException)

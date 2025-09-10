from fastapi import APIRouter, status, HTTPException, Depends
from app.schema.UserSchema import (
    UserListOutput, 
    UserInput, 
    LoginRequest, 
    RefreshTokenRequest
)
from app.models.User import Users
from app.models.refreshToken import RefreshToken
from datetime import datetime, timedelta, timezone
from typing import List
from app.utils.hashPassword import hash, verifyPassword
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.utils.auth import (createAccessToken, createRefreshToken, verifyRefreshToken)
from dotenv import load_dotenv
import os

load_dotenv()

REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

router = APIRouter(
    prefix="/user"
)

@router.get("/", response_model=List[UserListOutput])
async def allUser():
    post = await Users.find_all().to_list()
    return post


@router.post("/", response_model=UserListOutput)
async def createUser(user: UserInput):
    existsUser = await Users.find_one({
    "$or": [
            {"email": user.email},
            {"userName": user.userName}
        ]
    })
    print(existsUser)
    if existsUser:
        if existsUser.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"Email '{user.email}' already exists"
            )
        if existsUser.userName == user.userName:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username '{user.userName}' already exists"
            )
    user.password = hash(user.password)
    data = Users(**user.model_dump())
    await data.insert()
    return data

@router.post("/login")
async def userLogin(userCredentials: LoginRequest):
    user = await Users.find_one({"email":userCredentials.email})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not verifyPassword(userCredentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    accessToken = createAccessToken({"user_id": str(user.id)})
    refreshToken = createRefreshToken({"user_id": str(user.id)})

    tokenDoc = RefreshToken(
        userId=str(user.id),
        token=refreshToken,
        expiresAt=datetime.now(timezone.utc) + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS)),
        revoked=False
    )

    await tokenDoc.insert()

    return {
        "accessToken": accessToken,
        "refreshToken": refreshToken,
        "tokenType": "bearer"
    }

@router.post("/refreshToken")
async def get_new_access_token(request: RefreshTokenRequest):
    userData = verifyRefreshToken(request.refreshToken)
    storedToken = await RefreshToken.find_one({
        "token":request.refreshToken, "revoked":False
    })

    if not storedToken:
        raise HTTPException(status_code=401, detail="Refresh token expired or revoked")
    
    expiresAt = storedToken.expiresAt
    if expiresAt.tzinfo is None:
        expiresAt = expiresAt.replace(tzinfo=timezone.utc)

    if expiresAt < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired or revoked")
    
    storedToken.revoked = True
    await storedToken.save()

    newAccessToken = createAccessToken(data={"user_id": userData.id})
    newRefreshToken = createRefreshToken(data={"user_id": userData.id})
    
    tokenDoc = RefreshToken(
        userId=str(userData.id),
        token=newRefreshToken,
        expiresAt=datetime.now(timezone.utc) + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS)),
        revoked=False
    )

    await tokenDoc.insert()

    return {
        "access_token": newAccessToken,
        "refresh_token": newRefreshToken,
        "token_type": "bearer"
    }

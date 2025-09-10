from fastapi import APIRouter, status, HTTPException, Depends
from app.schema.UserSchema import (
    UserListOutput, 
    UserInput, 
    LoginRequest, 
    RefreshTokenRequest
)
from app.models.User import Users
from typing import List
from app.utils.hashPassword import hash, verifyPassword
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.utils.auth import (createAccessToken, createRefreshToken, verifyRefreshToken)

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

    return {
        "accessToken": accessToken,
        "refreshToken": refreshToken,
        "tokenType": "bearer"
    }

@router.post("/refreshToken")
async def get_new_access_token(request: RefreshTokenRequest):
    user_data = verifyRefreshToken(request.refreshToken)
    new_access_token = createAccessToken(data={"user_id": user_data.id})
    new_refresh_token = createRefreshToken(data={"user_id": user_data.id})
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

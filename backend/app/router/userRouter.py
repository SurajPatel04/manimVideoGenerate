from fastapi import (
    APIRouter, 
    status, 
    HTTPException,
    Depends,
    Query
)
from app.schema.UserSchema import (
    UserListOutput, 
    UserInput, 
    LoginRequest, 
    RefreshTokenRequest
)
from app.utils.auth import (
    createAccessToken, 
    createRefreshToken, 
    verifyRefreshToken
)
from app.utils.hashPassword import (
    hash, 
    verifyPassword
)
from datetime import (
    datetime, 
    timedelta, 
    timezone
)
from app.schema.UserSchema import TokenData
from bson import ObjectId
from app.models.User import Users
from app.models.UserHistory import UsersHistory
from app.models.RefreshToken import RefreshToken
from typing import List
from app.utils.auth import getCurrentUser
from dotenv import load_dotenv
import os

load_dotenv()

REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

router = APIRouter(
    prefix="/api/user"
)

@router.get("/", response_model=List[UserListOutput])
async def allUser():
    post = await Users.find_all().to_list()
    return post


@router.post("/signUp", response_model=UserListOutput, status_code=status.HTTP_201_CREATED)
async def createUser(user: UserInput):
    existsUser = await Users.find_one({
    "$or": [
            {"email": user.email},
        ]
    })
    print(existsUser)
    if existsUser:
        if existsUser.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"Email already exists"
            )
        
    user.password = hash(user.password)
    data = Users(**user.model_dump())
    await data.insert()
    return data

@router.post("/login", status_code=status.HTTP_200_OK)
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
        "email": user.email,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "userId": str(user.id),
        "tokenType": "bearer"
    }

@router.post("/refreshToken", status_code=status.HTTP_201_CREATED)
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
        "email":request.email,
        "token_type": "bearer"
    }

from bson import ObjectId


@router.get("/userHistory", status_code=status.HTTP_200_OK)
async def getUserHistory(
    current_user: TokenData = Depends(getCurrentUser),
    page: int = Query(1, ge=1),   # page number (default = 1, must be >= 1)
    limit: int = Query(5, ge=1, le=100)  # items per page (default = 5)
):
    user_id = ObjectId(current_user.id)

    skip = (page - 1) * limit

    # Fetch paginated history
    history = (
        await UsersHistory.find(UsersHistory.userId == user_id)
        .skip(skip)
        .limit(limit)
        .to_list()
    )

    total = await UsersHistory.find(UsersHistory.userId == user_id).count()

    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user history found"
        )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "pages": (total + limit - 1) // limit,  # ceil division
        "data": history
    }
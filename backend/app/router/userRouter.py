from fastapi import (
    APIRouter, 
    status, 
    HTTPException,
    Depends,
    Query
)
from app.schema.UserSchema import (
    UserInput, 
    UserOutput,
    LoginRequest, 
    RefreshTokenRequest,
    PasswordReset
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
from app.schema.UserSchema import TokenData, EmailModel
from bson import ObjectId
from app.models.User import Users
from app.models.UserHistory import UsersHistory
from app.models.RefreshToken import RefreshToken
from typing import List
from app.utils.auth import getCurrentUser
from app.config import Config
from app.core.mail import mail, createMessage
from app.utils.verification import createUrlSafeToken, decodeUrlSafeToken
from app.core.templates import render_template
from app.services.updateUser import UserService
from itsdangerous import BadSignature, SignatureExpired
from fastapi_mail import MessageSchema
from pathlib import Path
from fastapi.responses import RedirectResponse

REFRESH_TOKEN_EXPIRE_DAYS = int(Config.REFRESH_TOKEN_EXPIRE_DAYS)

router = APIRouter(
    prefix="/api/user"
)

@router.get("/", response_model=List[UserOutput])
async def allUser():
    post = await Users.find_all().to_list()
    return post



@router.post("/signUp", status_code=status.HTTP_201_CREATED)
async def createUser(user: UserInput):
    existsUser = await Users.find_one({"email": user.email})

    if existsUser:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Email already exists"
        )
        
    user.password = hash(user.password)
    data = Users(**user.model_dump())
    await data.insert()

    token = createUrlSafeToken({"email":user.email})
    link = f"http://{Config.DOMAIN}/api/user/verify/{token}"

    html_message = render_template(
        "emailVerification.html",
        link=link,
        username=user.email,
    )

    base_dir = Path(__file__).resolve().parent.parent.parent 
    
    gif_path = base_dir / "app" / "assets" / "ManimVideo.gif"

    if not gif_path.is_file():
        raise HTTPException(
            status_code=500, 
            detail=f"GIF file not found at path: {gif_path}"
        )

    message = MessageSchema(
        recipients=[user.email],
        subject="Verify Email",
        body=html_message,
        subtype="html",
        attachments=[{
            # 4. Convert the Path object to a string
            "file": str(gif_path),
            "headers": {
                "Content-ID": "<logogif>" 
            },
            "subtype": "gif"
        }]
    )

    await mail.send_message(message=message)
    return {
    "status": True,
    "message": "Account created successfully! Please check your email to verify your account."
}


@router.post("/login", status_code=status.HTTP_200_OK)
async def userLogin(userCredentials: LoginRequest):
    user = await Users.find_one({"email":userCredentials.email})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if user.isVerified == False:
        token = createUrlSafeToken({"email":user.email})
        link = f"http://{Config.DOMAIN}/api/user/verify/{token}"

        html_message = render_template(
            "emailVerification.html",
            link=link,
            username=user.email,
        )

        base_dir = Path(__file__).resolve().parent.parent.parent 
        
        gif_path = base_dir / "app" / "assets" / "ManimVideo.gif"

        if not gif_path.is_file():
            raise HTTPException(
                status_code=500, 
                detail=f"GIF file not found at path: {gif_path}"
            )

        message = MessageSchema(
            recipients=[user.email],
            subject="Verify Email",
            body=html_message,
            subtype="html",
            attachments=[{
                # 4. Convert the Path object to a string
                "file": str(gif_path),
                "headers": {
                    "Content-ID": "<logogif>" 
                },
                "subtype": "gif"
            }]
        )

        await mail.send_message(message=message)
        return {
            "error": "account_not_verified",
            "message": "Please verify your email address. Check your inbox.",
            "user":UserOutput(**user.model_dump())
        }
        
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


@router.get("/userHistory", status_code=status.HTTP_200_OK)
async def getUserHistory(
    current_user: TokenData = Depends(getCurrentUser),
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=100)
):
    user_id = ObjectId(current_user.id)

    skip = (page - 1) * limit

    history = (
        await UsersHistory.find(UsersHistory.userId == user_id)
        .sort("-createdAt")
        .skip(skip)
        .limit(limit)
        .to_list()
    )

    total = await UsersHistory.find(UsersHistory.userId == user_id).count()

    if not history:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No user history found"
        )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "pages": (total + limit - 1) // limit,
        "data": history
    }


@router.post("/sendMail")
async def sendMail(emails: EmailModel):
    emails = emails.addresses

    html = "<h1>Welcome to the app</h1>"
    message = createMessage(
        recipients=emails,
        subject="Welcome",
        body=html
    )

    await mail.send_message(message=message)

    return {"message":"Email sent successfully"}



@router.get("/verify/{token}", status_code=status.HTTP_200_OK)
async def verifyUserAccount(token: str):
    try:
        # Decode token with expiration handling
        tokenData = decodeUrlSafeToken(token, max_age=86400)  # 1 hour expiration
        userEmail = tokenData.get("email")
        if not userEmail:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token payload"
            )

    except SignatureExpired:
        # Token has expired
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired. Please request a new verification email."
        )
    except BadSignature:
        # Token is invalid or tampered
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    await UserService.verifyUserByEmail(userEmail)
    return RedirectResponse(url="http://localhost:5173/login?verified=success")


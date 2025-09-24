from fastapi import (
    APIRouter, 
    status, 
    HTTPException,
    Depends,
    Query,
    Request
)
from app.schema.UserSchema import (
    UserInput, 
    UserOutput,
    LoginRequest, 
    RefreshTokenRequest,
    PasswordResetRequest,
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
from fastapi.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config as StarletteConfig
import os
from dotenv import load_dotenv
load_dotenv()



REFRESH_TOKEN_EXPIRE_DAYS = int(Config.REFRESH_TOKEN_EXPIRE_DAYS)

router = APIRouter(
    prefix="/api/user"
)
starlette_config = StarletteConfig(environ={
    "GOOGLE_CLIENT_ID": Config.GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET": Config.GOOGLE_CLIENT_SECRET,
})

oauth = OAuth(starlette_config)

oauth.register(
    name="google",
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
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
    link = f"{Config.DOMAIN}/api/user/verify/{token}"

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
        link = f"{Config.DOMAIN}/api/user/verify/{token}"

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
            "isVerified":False,
            "error": "Account not verified",
            "message": "Please verify your email address. Check your inbox.",
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

    # Set tokens as HttpOnly cookies (same behavior as Google OAuth callback)
    is_secure = os.getenv("ENV", "development") == "production"
    samesite = "none" if is_secure else "lax"

    response = JSONResponse({
        "email": user.email,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "userId": str(user.id),
    })
    response.set_cookie("accessToken", accessToken, httponly=True, secure=is_secure, samesite=samesite, max_age=86400, path="/")
    response.set_cookie("refreshToken", refreshToken, httponly=True, secure=is_secure, samesite=samesite, max_age=604800, path="/")

    return response


@router.get("/userHistory", status_code=status.HTTP_200_OK)
async def getUserHistory(
    current_user: TokenData = Depends(getCurrentUser),
    page: int = Query(1, ge=1),
    limit: int = Query(15, ge=1, le=100)
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


@router.post('/logout')
async def logout(request: Request):
    """Clear HttpOnly auth cookies on logout."""
    response = JSONResponse({"status": True, "message": "Logged out"})
    # Clear cookies by setting empty value and max_age=0
    response.delete_cookie("accessToken", path="/")
    response.delete_cookie("refreshToken", path="/")
    return response


@router.post("/passwordResetRequest")
async def passwordChangeRequest(user: PasswordResetRequest):
    email = await Users.find_one({"email":user.email})
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account with this email"
        )
    token = createUrlSafeToken({"email":user.email})
    base_dir = Path(__file__).resolve().parent.parent.parent 
    gif_path = base_dir / "app" / "assets" / "ManimVideo.gif"

    if not gif_path.is_file():
        raise HTTPException(
            status_code=500, 
            detail=f"GIF file not found at path: {gif_path}"
        )
    if email.isVerified == False:
        link = f"{Config.DOMAIN}/api/user/verify/{token}"

        html_message = render_template(
            "emailVerification.html",
            link=link,
            username=user.email,
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
            "isVerified":False,
            "error": "Account not verified",
            "message": "Please verify your email address. Check your inbox.",
        }
    
    link = f"{Config.DOMAIN}/resetPassword/token={token}"

    html_message = render_template(
        "passwordRequest.html",
        link=link,
        username=user.email,
    )

    message = MessageSchema(
        recipients=[user.email],
        subject="Password Change Request Email",
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
        "message": "Please check your email to reset your password."
    }

@router.post("/resetPassword")
async def changePassword(userData: PasswordReset):
    print(userData.token)
    tokenData = decodeUrlSafeToken(userData.token, max_age=600)
    print(tokenData.get("email"))
    userEmail = tokenData.get("email")
    if not userEmail:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token payload"
            )

    user = await Users.find_one(Users.email == userEmail)
    
    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not Found"
        )

    password = hash(userData.password)
    user.password = password
    await user.save()
    return {
        "status": True,
        "message": "Password has been reset successfully."
    }
    

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
    return RedirectResponse(url=f"{Config.DOMAIN}/login?verified=success")


@router.get("/validateResetToken")
async def validateResetToken(token: str):
    """Validate a password-reset token without performing any account changes.

    Returns the email contained in the token when valid. Responds with clear
    HTTP errors when token is invalid or expired so the frontend can show
    an appropriate UI.
    """
    try:
        tokenData = decodeUrlSafeToken(token, max_age=600)
        userEmail = tokenData.get("email")
        if not userEmail:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token payload"
            )
    except SignatureExpired:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired. Please request a new password reset link."
        )
    except BadSignature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    user = await Users.find_one(Users.email == userEmail)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {"status": True, "email": userEmail}

@router.get("/google/login")
async def googleLogin(request: Request):
    redirect_uri = request.url_for("googleCallback")
    return await oauth.google.authorize_redirect(request, redirect_uri)



@router.get("/google/callback")
async def googleCallback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    userInfo = token.get("userinfo")
    if not userInfo:
        try:
            resp = await oauth.google.get("userinfo", token=token)
            userInfo = await resp.json()
        except Exception as e:
            raise HTTPException(status_code=400, detail="Google login failed: could not fetch userinfo")

    # Extract Google user details
    email = userInfo["email"]
    first_name = userInfo.get("given_name", "")
    last_name = userInfo.get("family_name", "")

    # Check if user already exists in DB
    user = await Users.find_one(Users.email == email)

    if not user:
        # Create new user
        user = Users(
            firstName=first_name,
            lastName=last_name,
            email=email,
            password="",  # not needed for Google users
            isVerified=True
        )
        await user.insert()

    # Issue your own JWT tokens
    access_token = createAccessToken({"user_id": str(user.id)})
    refresh_token = createRefreshToken({"user_id": str(user.id)})

    # Determine secure and samesite cookie attributes based on runtime.
    # For local HTTP development we avoid Secure=True (browsers will drop those cookies).
    is_secure = os.getenv("ENV", "development") == "production"
    samesite = "none" if is_secure else "lax"

    response = RedirectResponse(url=f"{Config.FRONTEND_DOMAIN}/main", status_code=302)
    # Set both cookies consistently
    response.set_cookie("accessToken", access_token, httponly=True, secure=is_secure, samesite=samesite, max_age=86400)
    response.set_cookie("refreshToken", refresh_token, httponly=True, secure=is_secure, samesite=samesite, max_age=604800)

    return response


@router.get("/me")
async def get_current_user_profile(current_user: TokenData = Depends(getCurrentUser)):
    """Return basic profile for the currently authenticated user.
    This endpoint is intended for the SPA to call after OAuth redirect to
    confirm that the HttpOnly cookie-based session is active.
    """
    # current_user is a TokenData instance with id set by getCurrentUser
    user = await Users.find_one({"_id": ObjectId(current_user.id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "email": user.email,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "userId": str(user.id),
    }


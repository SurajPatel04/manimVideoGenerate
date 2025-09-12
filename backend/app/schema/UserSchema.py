from pydantic import (
    BaseModel, 
    Field, 
    EmailStr
)
from typing import Optional

class UserListOutput(BaseModel):
    id: str
    email: str
    firstName: str
    lastName: Optional[str] = None

class UserInput(BaseModel):
    email: str
    password: str = Field(min_length=6)
    firstName: str
    lastName: Optional[str] = None

class TokenData(BaseModel):
    id: Optional[str]=None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    refreshToken: str
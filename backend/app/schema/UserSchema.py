from pydantic import (
    BaseModel, 
    Field, 
    EmailStr
)
from typing import Optional, List
from beanie import PydanticObjectId 

class UserListOutput(BaseModel):
    id: PydanticObjectId
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

class EmailModel(BaseModel):
    addresses: List[str]
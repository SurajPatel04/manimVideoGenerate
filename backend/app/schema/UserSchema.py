from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserListOutput(BaseModel):
    userName: str
    email: str

class UserInput(BaseModel):
    email: str
    password: str = Field(min_length=6)
    userName: str

class Token(BaseModel):
    id: Optional[str]=None

class LoginRequest(BaseModel):
    email: str
    password: str
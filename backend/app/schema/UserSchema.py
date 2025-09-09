from pydantic import BaseModel

class UserListOutput(BaseModel):
    name: str
    email: str

class UserInput(BaseModel):
    name: str
    email: str
    password: str
    userName: str
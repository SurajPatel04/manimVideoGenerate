from fastapi import APIRouter
from app.schema.UserSchema import UserListOutput, UserInput
from app.models.User import User
from typing import List

router = APIRouter(
    prefix="/user"
)

@router.get("/", response_model=List[UserListOutput])
async def allUser():
    post = await User.find_all().to_list()
    return post

@router.post("/", response_model=UserListOutput)
async def createUser(user: UserInput):
    data = User(**user.model_dump())
    await data.create()
    return data
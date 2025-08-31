from pydantic import BaseModel

class MainmUserModel(BaseModel):
    userQuery: str
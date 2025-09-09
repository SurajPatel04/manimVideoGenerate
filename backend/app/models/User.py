from beanie import Document
from pydantic import Field

class User(Document):
    name: str
    userName: str
    password: str
    email: str
    is_paid: bool = Field(default=False)
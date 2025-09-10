from beanie import Document, before_event, Replace, Update, Indexed
from pydantic import Field, EmailStr
from datetime import datetime, timezone
from typing import Annotated

class Users(Document):
    userName: Annotated[str, Indexed(unique=True)]
    password: str
    email: Annotated[EmailStr,Indexed(unique=True)]
    isPaid: bool = Field(default=False)
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @before_event([Replace, Update])
    def update_timestamp(self):
        self.updatedAt = datetime.now(timezone.utc)


    class Settings:
        name = "users"
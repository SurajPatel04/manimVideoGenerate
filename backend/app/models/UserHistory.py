from beanie import Document,Indexed
from bson import ObjectId
from datetime import datetime, timezone
from pydantic import Field, BaseModel
from typing import Optional, List, Annotated

class Message(BaseModel):
    userQuery: str
    description: Optional[str] = None
    code: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    filename: Optional[str]=None
    quality: Optional[str] = None
    link: Optional[str] = None

class UsersHistory(Document):
    userId: Annotated[ObjectId, Indexed()]
    chatName: Annotated[str, Indexed]
    messages: List[Message] = Field(default_factory=list)
    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str
        }
    }
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


    class Settings:
        name = "userHistory"
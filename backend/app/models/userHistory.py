from beanie import Document,Indexed
from bson import ObjectId
from datetime import datetime, timezone
from pydantic import Field, BaseModel
from typing import Optional, List, Annotated

class Message(BaseModel):
    userQuery: str
    AiResponse: Optional[str] = None
    code: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    link: Optional[str]=None
    qality: Optional[str] = str

class UsersHistory(Document):
    userId: Annotated[ObjectId, Indexed()]
    chatName: Annotated[str, Indexed]
    messages: List[Message] = []

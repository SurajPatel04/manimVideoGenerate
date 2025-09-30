from pydantic import BaseModel
from typing import Optional

class MainmUserModel(BaseModel):
    userQuery: str
    quality: str
    format: str
    historyId: Optional[str] = None
    resolution: str

class CancelRequest(BaseModel):
    taskId: str
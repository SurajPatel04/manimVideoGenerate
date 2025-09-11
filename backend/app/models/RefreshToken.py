from beanie import (
    Document, 
    Indexed
)
from datetime import (
    datetime, 
    timezone
)
from typing import Annotated
from pydantic import Field


class RefreshToken(Document):
    userId: Annotated[str, Indexed()]
    token: Annotated[str, Indexed(unique=True)]
    expiresAt: datetime
    revoked: bool = Field(default=False)
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "refresh_tokens"

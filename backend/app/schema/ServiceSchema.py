from pydantic import BaseModel, Field
from typing import (
    Optional, 
    List
)

# descriptionGenerate Schema
class CodeGenPossibility(BaseModel):
    isFesible: bool
    reason: str
    chatName: str

class DescriptionGenerationState(BaseModel):
    userQuery:str
    reason: Optional[str] = None
    chatName: Optional[str] = None
    descriptions:list[str] = []
    detailedDescription: str
    descriptionRefine: int
    isGood: bool | None = None 
    AutoComplete: bool
    detailedDescriptionError: Optional[str] = None
    format: str = Field(default="Red", description="The render file format")


class isQueryPossible(BaseModel):
    userQuery: str
    chatName: Optional[str] = None
    isFesible: Optional[bool] = None
    reason: Optional[str] = None

class GenDescriptions(BaseModel):
    descriptions: list[str]

class DetailDescription(BaseModel):
    description: str

class CheckDetailedDescription(BaseModel):
    isThisGoodDescrription: bool
    detailedDescriptionError: str


# manimCodeGeneration Schema
class CheckMaimCode(BaseModel):
    isCodeGood: bool
    errorMessage: str


class mainmState(BaseModel):
    description: str
    isCodeGood: Optional[bool] = None
    filename: str
    format: str = Field(default="Red", description="The render file format")
    validationError: Optional[str] = None
    validationErrorHistory: List[str] = Field(default_factory=list)
    executionErrorHistory: List[str] = Field(default_factory=list)
    executionError: Optional[str] = None
    rewriteAttempts: int = 0 
    executionSuccess: Optional[bool] = None
    quality: str = "ql"
    createAgain: int = 0
    code: Optional[str] = None
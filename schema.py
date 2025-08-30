from pydantic import BaseModel, Field
from typing import Optional, List


# descriptionGenerate Schema
class CodeGenPossibility(BaseModel):
    isFesible: bool
    reason: str
    chatName: str

class DescriptionGenerationState(BaseModel):
    userQuery:str
    isFesible: bool | None = None
    reason: Optional[str] = None
    chatName: Optional[str] = None
    descriptions:list[str] = []
    pickedOne: str
    DescriptionRefine: int
    isGood: bool | None = None 
    AutoComplete: bool
    pickedOneError: Optional[str] = None
    format: str = Field(default="Red", description="The render file format")

class GenDescriptions(BaseModel):
    descriptions: list[str]

class DetailDescription(BaseModel):
    description: str

class CheckPickedDescription(BaseModel):
    isThisGoodDescrription: bool
    pickedOneError: str


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
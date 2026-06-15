from pydantic import BaseModel, Field
from typing import (
    Optional, 
    List,
    Literal,
    Any
)
from enum import Enum

class AnimationType(str, Enum):
    GRAPH2D = "GRAPH2D"
    COMPUTER_DATASTRUCTURE = "COMPUTER_DATASTRUCTURE"
    GRAPH3D = "GRAPH3D"
    STATISTICS = "STATISTICS"
    PHYSICS="PHYSICS"
    MOBILE_GRAPH2D="MOBILE_GRAPH2D"
    TEXT="TEXT"

# descriptionGenerate Schema
class CodeGenPossibility(BaseModel):
    isFeasible: bool
    reason: str
    chatName: str
    animationType: AnimationType

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
    animationType: AnimationType


class isQueryPossible(BaseModel):
    userQuery: str
    chatName: Optional[str] = None
    isFeasible: Optional[bool] = None
    animationType: Optional[AnimationType] = None
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


class MatchCheck(BaseModel):
    matches: bool = Field(description="True if the rendered frame matches the user description, False otherwise")
    reason: str = Field(description="A short reason explaining why it matches or mismatches")
    fix_suggestion: Optional[str] = Field(default="", description="If it mismatches, provide exact instructions on how the code should be modified to fix the issue.")

class mainmState(BaseModel):
    userQuery: str
    description: str
    isCodeGood: Optional[bool] = None
    filename: str
    format: str = Field(default="Red", description="The render file format")
    validationError: Optional[str] = None
    validationErrorHistory: List[str] = Field(default_factory=list)
    executionErrorHistory: List[Any] = Field(default_factory=list)
    executionError: Optional[Any] = None
    rewriteAttempts: int = 0 
    executionSuccess: Optional[bool] = None
    matchesRequest: Optional[bool] = None
    quality: str = "ql"
    createAgain: int = 0
    code: Optional[str] = None
    animationType: AnimationType
    resolution: str
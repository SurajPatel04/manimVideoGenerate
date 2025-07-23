from pydantic import BaseModel
from typing import Optional


# descriptionGenerate Schema
class DescriptionGenerationState(BaseModel):
    user_query:str
    descriptions:list[str] = []
    pickedOne: str
    DescriptionRefine: int
    is_good: bool | None = None 
    AutoComplete: bool
    pickedOneError: Optional[str] = None
class GenDescriptions(BaseModel):
    descriptions: list[str]

class PickOneDescription(BaseModel):
    description: str

class CheckPickedDescription(BaseModel):
    is_this_good_descrription: bool
    pickedOneError: str


# manimCodeGeneration Schema
class CheckMaimCode(BaseModel):
    is_code_good: bool
    error_message: str


class mainmState(BaseModel):
    description: str
    is_code_good: Optional[bool] = None
    filename: str
    error_message: Optional[str] = None
    rewrite_attempts: int = 0 
    execution_success: Optional[bool] = None
    quality: str = "ql"
from pydantic import BaseModel, Field
from typing import Optional, List


# descriptionGenerate Schema
class DescriptionGenerationState(BaseModel):
    user_query:str
    descriptions:list[str] = []
    pickedOne: str
    DescriptionRefine: int
    is_good: bool | None = None 
    AutoComplete: bool
    pickedOneError: Optional[str] = None
    format: str = Field(default="Red", description="The render file format")

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
    format: str = Field(default="Red", description="The render file format")
    validation_error: Optional[str] = None
    validation_error_history: List[str] = Field(default_factory=list)
    execution_error_history: List[str] = Field(default_factory=list)
    execution_error: Optional[str] = None
    rewrite_attempts: int = 0 
    execution_success: Optional[bool] = None
    quality: str = "ql"
    create_again: int = 0
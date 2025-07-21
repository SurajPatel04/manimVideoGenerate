from pydantic import BaseModel
from typing import Optional

class State(BaseModel):
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
from pydantic import BaseModel
from typing import Optional


class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    steps: str

class RecipeRequest(RecipeBase):
    ...

class RecipeResponse(RecipeBase):
    id: int

    class Config:
        orm_mode = True

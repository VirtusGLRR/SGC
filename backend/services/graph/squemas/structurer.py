from pydantic import BaseModel
from typing import List

class StructurerOutputSchema(BaseModel):
    nome: str
    ingredients: str
    preparation_method: str

class StructurerOutputSchemaList(BaseModel):
    recipes: List[StructurerOutputSchema]

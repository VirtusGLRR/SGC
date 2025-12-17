from pydantic import BaseModel
from typing import List

class IngredientItem(BaseModel):
    name: str
    amount: float
    measure_unity: str

class StructurerOutputSchema(BaseModel):
    title: str
    description: str
    steps: str
    ingredients: List[IngredientItem]

class StructurerOutputSchemaList(BaseModel):
    recipes: List[StructurerOutputSchema]

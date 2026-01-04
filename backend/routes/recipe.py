from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from controllers import RecipeController
from schemas import RecipeResponse, RecipeRequest
from database.database import get_db

recipe_routes = APIRouter()

@recipe_routes.post("/api/recipes", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create(request: RecipeRequest, db: Session = Depends(get_db)):
    return RecipeController.create(request, db)

@recipe_routes.get("/api/recipes", response_model=list[RecipeResponse])
def find_all_or_by_name(name: str | None = None, db: Session = Depends(get_db)):
    if name:
        return RecipeController.find_by_name(name, db)
    return RecipeController.find_all(db)

@recipe_routes.get("/api/recipes/{id}", response_model=RecipeResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    return RecipeController.find_by_id(id, db)

@recipe_routes.delete("/api/recipes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    return RecipeController.delete_by_id(id, db)

@recipe_routes.put("/api/recipes/{id}", response_model=RecipeResponse)
def update(id: int, request: RecipeRequest, db: Session = Depends(get_db)):
    return RecipeController.update(id, request, db)

@recipe_routes.get("/recipes/costs")
def get_all_recipe_costs(db: Session = Depends(get_db)):
    return RecipeController.get_all_recipes_with_cost(db)

@recipe_routes.get("/recipes/cost/{recipe_id}")
def get_recipe_cost(recipe_id: int, db: Session = Depends(get_db)):
    return RecipeController.get_recipe_cost(recipe_id, db)

@recipe_routes.get("/recipes/feasible")
def get_feasible_recipes(db: Session = Depends(get_db)):
    return RecipeController.get_feasible_recipes(db)

@recipe_routes.get("/recipes/popular-ingredients/{limit}")
def get_most_popular_ingredients(limit: int = 5, db: Session = Depends(get_db)):
    return RecipeController.get_most_used_ingredients(limit, db)
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from controllers import ItemController
from schemas import ItemResponse, ItemRequest
from database.database import get_db

item_routes = APIRouter()

@item_routes.post("/api/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create(request: ItemRequest, db: Session = Depends(get_db)):
    return ItemController.create(request, db)

@item_routes.get("/api/items", response_model=list[ItemResponse])
def find_all_or_by_name(name: str | None = None, db: Session = Depends(get_db)):
    if name:
        return ItemController.find_by_name(name, db)
    return ItemController.find_all(db)

@item_routes.get("/api/items/{id}", response_model=ItemResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    return ItemController.find_by_id(id, db)

@item_routes.delete("/api/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    return ItemController.delete_by_id(id, db)

@item_routes.put("/api/items/{id}", response_model=ItemResponse)
def update(id: int, request: ItemRequest, db: Session = Depends(get_db)):
    return ItemController.update(id, request, db)

@item_routes.get("/items/summary")
def get_items_summary(db: Session = Depends(get_db)):
    return ItemController.get_inventory_summary(db)

@item_routes.get("/items/total-value/{id}")
def get_total_item_value(id: int, db: Session = Depends(get_db)):
    return ItemController.get_total_item_value_by_id(id, db)

@item_routes.get("/items/low-stock/{threshold}")
def get_low_stock_items(threshold: int = 5, db: Session = Depends(get_db)):
    return ItemController.get_low_stock_items(threshold, db)

@item_routes.get("/items/expiring/{days_ahead}")
def get_items_near_expiration(days_ahead: int = 7, db: Session = Depends(get_db)):
    return ItemController.get_items_near_expiration(days_ahead, db)

@item_routes.get("/items/top-value/{top_n}")
def get_items_by_value_ranking(top_n: int = 5, db: Session = Depends(get_db)):
    return ItemController.get_items_by_value_ranking(top_n, db)
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    name: str
    measure_unity: str
    amount: float
    description: Optional[str] = None
    price: Optional[float] = 0
    expiration_date: Optional[str] = None
    create_date: Optional[str] = datetime.now()
    update_date: Optional[str] = None

class ItemRequest(ItemBase):
    ...

class ItemResponse(ItemBase):
    id: int

    class Config:
        orm_mode = True


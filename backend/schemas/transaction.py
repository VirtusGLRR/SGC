from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    item_id: int
    order_type: str
    description: str
   
    create_at: Optional[datetime] = Field(default_factory=datetime.now)
    
    amount: float
    price: Optional[float] = 0.0

class TransactionRequest(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
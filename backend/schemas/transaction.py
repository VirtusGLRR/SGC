from pydantic import BaseModel, ConfigDict, Field, computed_field
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

    @computed_field
    @property
    def item_name(self) -> Optional[str]:
        """Nome do item associado à transação"""
        # Será preenchido pelo controller se o item estiver carregado
        return getattr(self, '_item_name', None)

    model_config = ConfigDict(from_attributes=True)
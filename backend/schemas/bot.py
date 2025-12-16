from pydantic import BaseModel, ConfigDict
from typing import Optional
from datatime import datetime

class BotBase(BaseModel):
    Optional[str] = None
    user_message: str
    ai_message: Optional[str] = None
    create_at: Optional[datetime] = datetime.now()

class BotRequest():
    thread_id: Optional[str] = None
    user_message: str

class BotResponse(BotBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
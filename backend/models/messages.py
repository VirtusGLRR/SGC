from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from pydantic import BaseModel
from database.database import Base

class Message(Base):
    __tablename__ = "Message"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    thread_id = Column(String, nullable=False, index=True)
    user_message = Column(String, nullable=False)
    ai_message = Column(String, nullable=False)
    create_at = Column(String, nullable=False)
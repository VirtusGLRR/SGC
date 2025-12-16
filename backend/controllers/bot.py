from fastapi import Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database.database import get_db
from models import Bot
from services.graph.graph import graph
from repositories import BotRepository
from schemas import BotRequest, BotResponse

class BotController:
    @staticmethod
    async def process_message(request: BotRequest, db: Session = Depends(get_db)):
        message = BotRepository.save(db, Bot(**request.model_dump()))
        return BotResponse.model_validate(message)

    @staticmethod
    def get_all_messages(db: Session = Depends(get_db)):
        messages = BotRepository.get_messages(db)
        if not messages:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sem mensagens encontradas."
            )
        return [BotResponse.model_validate(message) for message in messages]
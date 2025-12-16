from sqlalchemy.orm import Session

from models import Bot

class BotRepository:
    @staticmethod
    def save_message(db: Session, thread_id: str, user_message: str, ai_message: str, create_at: str) -> Message:
        new_message = Bot(
            thread_id=thread_id,
            user_message=user_message,
            ai_message=ai_message,
            create_at=create_at
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message
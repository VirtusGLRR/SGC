from sqlalchemy.orm import Session

from models import Bot

class BotRepository:
    @staticmethod
    def save(db: Session, thread_id: str, user_message: str, ai_message: str, create_at: str) -> Message:
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

    @staticmethod
    def get_messages(db: Session):
        messages = db.query(Bot).all()
        if not messages:
            return None
        return messages
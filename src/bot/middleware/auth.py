from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
import structlog

from src.core.database.connection import get_db
from src.core.database.models import User as DBUser

logger = structlog.get_logger()

class AuthMiddleware(BaseMiddleware):
    """Authentication middleware to ensure user exists in database"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        # Get user from event
        user: User = data.get("event_from_user")
        if not user:
            return await handler(event, data)
        
        # Check if user exists in database
        with get_db() as db:
            db_user = db.query(DBUser).filter(DBUser.telegram_id == user.id).first()
            
            if not db_user:
                # Create new user
                db_user = DBUser(
                    telegram_id=user.id,
                    username=user.username,
                    first_name=user.first_name
                )
                db.add(db_user)
                db.commit()
                logger.info("New user auto-registered", telegram_id=user.id)
            
            # Add user to data context
            data["db_user"] = db_user
        
        return await handler(event, data)
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
import time
import structlog
from collections import defaultdict, deque

from src.core.config import settings

logger = structlog.get_logger()

class RateLimitMiddleware(BaseMiddleware):
    """Rate limiting middleware to prevent spam"""
    
    def __init__(self):
        self.user_requests = defaultdict(deque)
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        # Only apply to messages
        if not isinstance(event, Message):
            return await handler(event, data)
        
        user_id = event.from_user.id
        current_time = time.time()
        
        # Clean old requests
        user_queue = self.user_requests[user_id]
        while user_queue and current_time - user_queue[0] > settings.rate_limit_window:
            user_queue.popleft()
        
        # Check rate limit
        if len(user_queue) >= settings.rate_limit_requests:
            logger.warning("Rate limit exceeded", user_id=user_id)
            await event.answer("⚠️ Vous envoyez trop de messages. Attendez un moment avant de continuer.")
            return
        
        # Add current request
        user_queue.append(current_time)
        
        return await handler(event, data)

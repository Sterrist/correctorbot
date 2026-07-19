from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
from config import settings
import logging

logger = logging.getLogger('middleware.user')

class UserMiddleware(BaseMiddleware):
    async def __call__(self,
                 handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                 event: TelegramObject,
                 data: Dict[str, Any]) -> Any:

        if event.from_user is None:
            return

        if event.from_user.id not in settings.ADMIN_IDS:
            return

        return await handler(event, data)

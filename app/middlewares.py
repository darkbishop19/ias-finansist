from typing import Dict, Callable, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message


class BotObjectMiddleware(BaseMiddleware):

    def __init__(self, bot_object: Bot):
        super().__init__()
        self.bot_object = bot_object

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        data['bot_object'] = self.bot_object
        return await handler(event, data)

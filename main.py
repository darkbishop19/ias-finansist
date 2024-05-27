import json
import logging
import time
from aiogram import Bot, Dispatcher, types
from aiogram.methods import DeleteWebhook

from app.handlers import router
from app.admin_handlers import admin_router

from dotenv import load_dotenv
import os
import asyncio
import asyncpg
from app.middlewares import BotObjectMiddleware
load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
dp.include_routers(admin_router,
                   router)

dp.update.middleware(BotObjectMiddleware(bot_object=bot))

logging.basicConfig(level=logging.INFO)


async def handler(event, context):
    body = json.loads(event['body'])
    update = types.Update.parse_obj(body)
    await dp.feed_webhook_update(bot, update)


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

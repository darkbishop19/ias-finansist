import json
import logging
import time
from aiogram import Bot, Dispatcher, types
from app.handlers import router
from app.admin_handlers import admin_router

from dotenv import load_dotenv
import os
import asyncio
import asyncpg

load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
# BANK_DATABASE_URL = os.getenv('BANK_DATABASE_URL')
# SERVER_DATABASE_URL = os.getenv('SERVER_DATABASE_URL')
dp.include_routers(admin_router,
                   router)

logging.basicConfig(level=logging.INFO)


async def handler(event, context):
    body = json.loads(event['body'])
    update = types.Update.parse_obj(body)
    await dp.feed_webhook_update(bot, update)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

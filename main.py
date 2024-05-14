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
BANK_DATABASE_URL = os.getenv('BANK_DATABASE_URL')
SERVER_DATABASE_URL = os.getenv('SERVER_DATABASE_URL')
dp.include_routers(admin_router,
                   router)
global db_bank_pool, db_server_pool

logging.basicConfig(level=logging.INFO)

async def handler(event, context):
    body = json.loads(event['body'])
    update = types.Update.parse_obj(body)
    db_bank_pool = await asyncpg.create_pool(BANK_DATABASE_URL)
    db_server_pool = await asyncpg.create_pool(SERVER_DATABASE_URL)
    await dp.feed_webhook_update(bot, update)


async def main():
    # db_bank_pool = await asyncpg.create_pool(BANK_DATABASE_URL)
    # db_server_pool = await asyncpg.create_pool(SERVER_DATABASE_URL)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

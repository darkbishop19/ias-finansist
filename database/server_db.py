import asyncio
import os
import asyncpg
from dotenv import load_dotenv
from aiogram.types import Message
load_dotenv()

print(os.getenv('DB_HOST'))


async def create_pool():
    db_server_pool = await asyncpg.create_pool(database=os.getenv('DB_SERV_NAME'),
                                               host=os.getenv('DB_HOST'),
                                               port=os.getenv('DB_PORT'),
                                               user=os.getenv('DB_USER'),
                                               password=os.getenv('DB_PAS'))
    return db_server_pool


async def get_user_to_db(user_id: int):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query = f"SELECT * FROM telegram_users"
        result = await conn.fetch(query)
        print(result[0]['account_id'])
        await conn.close()


async def check_password(password):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        print(password)
        query_all = f'select * from telegram_users'
        print(await conn.fetch(query_all))
        query_get = (f"SELECT * FROM telegram_users "
                     f"WHERE password = '{password}'")
        result = await conn.fetch(query_get)
        await conn.close()
        return result[-1]



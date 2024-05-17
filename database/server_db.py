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


async def check_password(password):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM telegram_users "
                     f"WHERE password = '{password}'")
        result = await conn.fetch(query_get)
        await conn.close()
        return result[-1]


async def update_user_info(password, telegram_id, language_code, username):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_update = (f"UPDATE telegram_users "
                        f"SET telegram_id = '{telegram_id}', language_code = '{language_code}', username = '{username}' "
                        f"WHERE password = '{password}';")
        await conn.execute(query_update)
        print('bib')
        await conn.close()

async def create_session(telegra_user_id):
    pass
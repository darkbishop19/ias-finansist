import asyncio
import os
import asyncpg
from dotenv import load_dotenv
from aiogram.types import Message

load_dotenv()


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
        db_server_pool.terminate()
        return result[-1]


async def update_user_info(password, telegram_id, language_code, username):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_update = (f"UPDATE telegram_users "
                        f"SET telegram_id = '{telegram_id}', language_code = '{language_code}', username = '{username}' "
                        f"WHERE password = '{password}';")
        await conn.execute(query_update)
        db_server_pool.terminate()
        await conn.close()


async def create_session(telegram_user_id, moscow_time):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_post = (f"INSERT INTO sessions "
                      f"(telegram_user_id, create_date, status) "
                      f"VALUES ({telegram_user_id}, '{moscow_time}', 'активен');"
                      )
        await conn.execute(query_post)
        query_get = (f"SELECT * "
                     f"FROM sessions "
                     f"WHERE    telegram_user_id = {telegram_user_id} "
                     f"ORDER BY session_id desc "
                     f"LIMIT 1;"
                     )
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result[-1]['session_id']


async def end_session(session_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_update = (f"UPDATE sessions "
                        f"SET status = 'завершен' "
                        f"WHERE session_id = {session_id};")
        await conn.execute(query_update)
        await conn.close()
        db_server_pool.terminate()


async def get_session_item(session_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f'SELECT * '
                     f'FROM sessions '
                     f"WHERE session_id = {session_id} and status = 'активен'")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result[-1]


async def get_telegram_user_item(telegram_user_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f'SELECT * '
                     f'FROM telegram_users '
                     f'WHERE telegram_user_id = {telegram_user_id}')
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result[-1]


async def create_report(session_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_post = (f"INSERT INTO reports "
                      f"(session_id, create_date, status) "
                      f"VALUES ({session_id}, CURRENT_TIMESTAMP,  'процесс');"
                      )
        await conn.execute(query_post)
        query_get = (f"SELECT * "
                     f"FROM reports "
                     f"WHERE   session_id  = {session_id} "
                     f"ORDER BY create_date desc "
                     f"LIMIT 1;"
                     )
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result[-1]


async def update_report_status(report_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_update = (f"UPDATE reports "
                        f"SET status = 'завершен' "
                        f"WHERE report_id = {report_id};")
        await conn.execute(query_update)
        await conn.close()
        db_server_pool.terminate()


async def get_user_session_items(telegram_user_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f'SELECT * '
                     f'FROM sessions '
                     f'WHERE telegram_user_id = {telegram_user_id}')
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result


async def get_session_report_items(session_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f'SELECT * '
                     f'FROM reports '
                     f'WHERE session_id = {session_id}')
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result


async def get_sessions_count():
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f'SELECT count(*) '
                     f'FROM sessions; ')
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result


async def get_reports_count():
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f'SELECT count(*) '
                     f'FROM reports; ')
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result


async def get_users_count():
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f'SELECT count(*) '
                     f'FROM telegram_users; ')
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result


async def update_user_role(telegram_user_id, role):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_update = (f"UPDATE telegram_users "
                        f"SET role = '{role}' "
                        f"WHERE telegram_user_id = {telegram_user_id};")
        await conn.execute(query_update)
        await conn.close()
        db_server_pool.terminate()

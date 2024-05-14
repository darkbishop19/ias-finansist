import asyncio
import os
import psycopg2
import asyncpg
from dotenv import load_dotenv
load_dotenv()


print(os.getenv('DB_HOST'))
async def get_user_to_db(user_id: int):
    db_server_pool = await asyncpg.create_pool(database=os.getenv('DB_SERV_NAME'),
                        host=os.getenv('DB_HOST'),
                        port=os.getenv('DB_PORT'),
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PAS'))
    async with db_server_pool.acquire() as conn:
        query = f"SELECT * FROM telegram_users"
        result = await conn.fetch(query)
        print(result[0]['account_id'])
        await conn.close()
if __name__ == "__main__":
    asyncio.run(get_user_to_db(734434528))
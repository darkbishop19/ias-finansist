import asyncio
import os
import asyncpg
from dotenv import load_dotenv
from aiogram.types import Message

load_dotenv()


async def create_pool():
    db_server_pool = await asyncpg.create_pool(database=os.getenv('DB_BANK_NAME'),
                                               host=os.getenv('DB_HOST'),
                                               port=os.getenv('DB_PORT'),
                                               user=os.getenv('DB_USER'),
                                               password=os.getenv('DB_PAS'))
    return db_server_pool


async def get_account_loans(account_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM loans "
                     f"WHERE account_id = {account_id}")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result


async def get_account_loan_payments(loan_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM loan_invoices "
                     f"WHERE loan_id = '{loan_id}'")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result


async def get_loan_type(loan_type_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM loan_types "
                     f"WHERE loan_type_id = '{loan_type_id}'")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result[-1]


async def get_loan_product(loan_product_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM loan_products "
                     f"WHERE loan_product_id = '{loan_product_id}'")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result[-1]


async def get_loan_item(loan_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM loans "
                     f"WHERE loan_id = '{loan_id}'")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result[-1]


async def get_account_deposits(account_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM deposits "
                     f"WHERE account_id = {account_id}")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result


async def get_deposit_invoices(deposit_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM deposit_invoices "
                     f"WHERE deposit_id = {deposit_id}")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result


async def get_deposit_item(deposit_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM deposits "
                     f"WHERE deposit_id = {deposit_id}")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result[-1]


async def get_deposit_product_item(deposit_product_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM deposit_products "
                     f"WHERE deposit_product_id = {deposit_product_id}")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result[-1]


async def get_deposit_type_item(deposit_type_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM deposit_types "
                     f"WHERE deposit_type_id = {deposit_type_id}")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result[-1]


async def get_account_item(account_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM accounts "
                     f"WHERE account_id = {account_id}")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result[-1]


async def get_account_deposit_items(account_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM deposits "
                     f"WHERE account_id = {account_id}")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result


async def get_all_bank_deposit_products():
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM deposit_products")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result


async def get_customer_item(customer_id):
    db_server_pool = await create_pool()
    async with db_server_pool.acquire() as conn:
        query_get = (f"SELECT * FROM customers "
                     f"WHERE customer_id = {customer_id}")
        result = await conn.fetch(query_get)
        await conn.close()
        db_server_pool.terminate()
        return result[-1]

from aiogram.fsm.context import FSMContext
from analysis import reports
from database import server_db, object_storage
from app.fsm import Consultant
from assets import text_samples
from aiogram import types, F, Router
from dotenv import load_dotenv
from aiogram.types import Message, BufferedInputFile


load_dotenv()
analyst_router = Router()


@analyst_router.message(F.text == text_samples.get_metrics)
async def get_metrics(message: Message):
    sessions_count = await server_db.get_sessions_count()
    reports_count = await server_db.get_sessions_count()
    users_count = await server_db.get_users_count()
    text = f'Количество сессий пользователей: <code>{sessions_count[-1]["count"]}</code>\n' \
           f'Количество отчетов пользователей: <code>{reports_count[-1]["count"]}</code>\n' \
           f'Количество пользователей в системе: <code>{users_count[-1]["count"]}</code>'
    await message.answer(text, parse_mode='HTML')

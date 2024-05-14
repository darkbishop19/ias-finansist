import os

from aiogram import types, F, Router
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv

load_dotenv()
admin_router = Router()
admin_id = os.getenv('ADMIN_ID')


@admin_router.message(Command('admin'))
async def cmd_admin(message: types.Message):
    print('works')
    if str(message.from_user.id) == admin_id:
        print('works')
        await message.answer(text='Админ панель включилась', parse_mode='HTML')

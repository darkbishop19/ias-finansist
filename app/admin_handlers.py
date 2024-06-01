import os

from aiogram.fsm.context import FSMContext
from database import server_db, bank_db, object_storage
from app.fsm import NextStep, Admin
from assets import text_samples, adaptive_text
from aiogram import types, F, Router
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv
from aiogram.types import Message, FSInputFile, BufferedInputFile, CallbackQuery
from app import markups

load_dotenv()
admin_router = Router()
admin_id = os.getenv('ADMIN_ID')


@admin_router.message(Command('admin'))
async def cmd_admin(message: types.Message):
    print('works')
    if str(message.from_user.id) == admin_id:
        print('works')
        await message.answer(text='Админ панель включилась', parse_mode='HTML')


@admin_router.message(F.text == text_samples.check_profile)
async def request_telegram_user_id(message: Message, state: FSMContext):
    await message.answer(text_samples.type_user_id)
    await state.set_state(Admin.telegram_user_id)


@admin_router.message(Admin.telegram_user_id)
async def get_user_info(message: Message, state: FSMContext):
    await state.clear()
    try:
        telegram_user_id = int(message.text)
        user_text = await adaptive_text.get_all_users_info(telegram_user_id)
        await message.answer(user_text, parse_mode='HTML',
                             reply_markup=await markups.change_role(telegram_user_id))
    except:
        await message.answer(text_samples.user_not_found)


@admin_router.callback_query(F.data.startswith('changerole'))
async def choose_role(call: CallbackQuery):
    operation, telegram_user_id = call.data.split('_')
    await call.message.edit_text(text=await adaptive_text.get_all_users_info(int(telegram_user_id)),
                                 reply_markup=await markups.choose_role(telegram_user_id),
                                 parse_mode='HTML')


@admin_router.callback_query(F.data.startswith('make'))
async def change_role(call: CallbackQuery):
    operation, telegram_user_id = call.data.split('_')
    role = ''
    if operation == 'makeclient':
        role = 'клиент'
    elif operation == 'makeanalyst':
        role = 'аналитик'
    elif operation == 'makeconsult':
        role = 'консультант'
    elif operation == 'makeadmin':
        role = 'администратор'

    await server_db.update_user_role(int(telegram_user_id), role)
    await call.message.answer(text_samples.change_role_success)
    await call.message.edit_reply_markup(reply_markup=await markups.change_role(telegram_user_id))

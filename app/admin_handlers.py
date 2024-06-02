from aiogram.fsm.context import FSMContext
from database import server_db, object_storage
from app.fsm import Admin
from assets import text_samples, adaptive_text
from aiogram import F, Router
from dotenv import load_dotenv
from aiogram.types import Message, BufferedInputFile, CallbackQuery
from app import markups

load_dotenv()
admin_router = Router()


@admin_router.message(F.text == text_samples.check_profile)
async def request_telegram_user_id(message: Message, state: FSMContext):
    await message.answer(text_samples.type_user_id)
    await state.set_state(Admin.telegram_user_id)


@admin_router.message(F.text == text_samples.check_reports)
async def request_telegram_user_id(message: Message, state: FSMContext):
    await message.answer(text_samples.type_report_id)
    await state.set_state(Admin.report_id)


@admin_router.message(Admin.report_id)
async def get_report(message: Message, state: FSMContext):
    await state.clear()
    try:
        report_id = int(message.text)
        pdf_report = await object_storage.get_report(report_id)
        await message.answer_document(document=BufferedInputFile(file=pdf_report,
                                                                 filename=f'Финансовая консультация {report_id}.pdf'))
    except:
        await message.answer(text_samples.report_not_found)


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

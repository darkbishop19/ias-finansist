from aiogram import types, F, Router, Bot
from aiogram.filters import CommandStart, Command
from app import markups
from aiogram.fsm.context import FSMContext
from database import server_db, object_storage, bank_db
from aiogram.types import Message, FSInputFile, BufferedInputFile, CallbackQuery
from assets import adaptive_text, text_samples
from app.fsm import NextStep, Session
from app import functions
from analysis import reports
from asyncpg import Record

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(text=await adaptive_text.hello_text(message.from_user.username), parse_mode='HTML'
                         )
    await state.set_state(NextStep.password)


@router.message(Command('end'))
async def end_session(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    session_id = state_data.get('session_id')
    try:
        session_item = await server_db.get_session_item(int(session_id))
    except:
        await message.answer(text_samples.session_not_found)
        return
    await server_db.end_session(session_id)
    await state.clear()
    await message.answer(text_samples.session_ends)


@router.message(Command('help'))
async def cmd_start(message: types.Message):
    await message.answer(text='Помощь', parse_mode='HTML')


@router.message(F.text == text_samples.consulting)
async def cmd_start(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    session_id = state_data.get('session_id')
    try:
        session_item = await server_db.get_session_item(int(session_id))
    except:
        await message.answer(text_samples.session_not_found)
        return

    await message.answer(text_samples.report_creation_started)

    telegram_user_item = await server_db.get_telegram_user_item(session_item['telegram_user_id'])
    report = await server_db.create_report(session_id)
    await reports.create_account_financial_consulting_report(telegram_user_item['account_id'], report['report_id'])
    pdf_report = await object_storage.get_report(report['report_id'])
    await message.answer_document(document=BufferedInputFile(file=pdf_report,
                                                             filename=f'Финансовая консультация {report["report_id"]}.pdf'))


@router.message(F.text == text_samples.profile)
async def show_profile_info(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    session_id = state_data.get('session_id')
    try:
        session_item = await server_db.get_session_item(int(session_id))
    except:
        await message.answer(text_samples.session_not_found)
        return
    await message.answer(await adaptive_text.get_profile_info(session_item["telegram_user_id"]),
                         parse_mode='HTML',
                         reply_markup=await markups.client_subs_to_notifications(session_item["telegram_user_id"]))


@router.message(F.text == text_samples.support)
async def show_support_info(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    session_id = state_data.get('session_id')
    try:
        session_item = await server_db.get_session_item(int(session_id))
    except:
        await message.answer(text_samples.session_not_found)
        return
    await message.answer(text_samples.support_description,
                         parse_mode='HTML')


@router.message(F.text == text_samples.reports)
async def show_profile_info(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    session_id = state_data.get('session_id')
    try:
        session_item = await server_db.get_session_item(int(session_id))
    except:
        await message.answer(text_samples.session_not_found)
        return
    await message.answer(text_samples.your_reports,
                         parse_mode='HTML',
                         reply_markup=await markups.get_user_reports(session_item["telegram_user_id"]))


@router.message(F.text == text_samples.sessions)
async def show_user_sessions(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    session_id = state_data.get('session_id')
    try:
        session_item = await server_db.get_session_item(int(session_id))
    except:
        await message.answer(text_samples.session_not_found)
        return
    await message.answer(text_samples.your_sessions,
                         reply_markup=await markups.get_user_sessions(session_item["telegram_user_id"]))


@router.callback_query(F.data.startswith('showreport'))
async def send_report_to_user(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    session_id = state_data.get('session_id')
    try:
        session_item = await server_db.get_session_item(int(session_id))
    except:
        await call.message.answer(text_samples.session_not_found)
        return

    operation, report_id = call.data.split('_')
    pdf_report = await object_storage.get_report(int(report_id))
    await call.message.reply_document(document=BufferedInputFile(file=pdf_report,
                                                                 filename=f'Финансовая консультация {report_id}.pdf'))


@router.callback_query(F.data.startswith('notifsub'))
async def send_report_to_user(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    session_id = state_data.get('session_id')
    try:
        session_item = await server_db.get_session_item(int(session_id))
    except:
        await call.message.answer(text_samples.session_not_found)
        return
    operation, telegram_user_id = call.data.split('_')
    telegram_user_item = await server_db.get_telegram_user_item(int(telegram_user_id))
    try:
        notification_item = await bank_db.get_notification_item(telegram_user_item['account_id'])
        if notification_item['status'] == 'активен':
            message_text = f'{text_samples.already_notification_sub}'
        else:
            message_text = f'{text_samples.success_notification_sub}'
            await bank_db.update_notification_item(telegram_user_item['account_id'])
    except:
        message_text = f'{text_samples.success_notification_sub}'
        await bank_db.create_notification_item(telegram_user_item['account_id'])
    await call.message.answer(message_text)


@router.callback_query(F.data.startswith('showsession'))
async def send_report_to_user(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    session_id = state_data.get('session_id')
    try:
        session_item = await server_db.get_session_item(int(session_id))
    except:
        await call.message.answer(text_samples.session_not_found)
        return
    operation, search_session_id = call.data.split('_')
    session_item = await server_db.get_session_item(int(search_session_id))
    text = f'Идентификатор сессии: <code>{session_item["session_id"]}</code>\n' \
           f'Дата создания: <code>{session_item["create_date"]}</code>\n' \
           f'Статус: <code>{session_item["status"]}</code>'
    await call.message.reply(text, parse_mode='HTML')


@router.message(NextStep.password)
async def password_check(message: Message, state: FSMContext, bot_object: Bot):
    try:
        server_user_item = await server_db.check_password(message.text)

        if server_user_item['telegram_id'] is not None and server_user_item['telegram_id'] != message.from_user.id:
            await bot_object.send_message(chat_id=server_user_item['telegram_id'], parse_mode='HTML',
                                          text=await adaptive_text.user_info_changed(message.from_user.id,
                                                                                     message.from_user.username,
                                                                                     message.date))
        elif server_user_item['telegram_id'] is None:
            await server_db.update_user_info(message.text, message.from_user.id, message.from_user.language_code,
                                             message.from_user.username)

        await message.answer(text=text_samples.password_success, parse_mode='HTML')
        await state.clear()
        await create_session(message, state, server_user_item['telegram_user_id'])
    except:
        await message.reply(text=text_samples.password_error, parse_mode='HTML')


async def create_session(message: Message, state: FSMContext, telegram_user_id: int):
    try:
        telegram_user_item = await server_db.get_telegram_user_item(telegram_user_id)
        moscow_time = await functions.get_message_moscow_time(message.date)
        session_id = await server_db.create_session(telegram_user_id, moscow_time)
        await state.set_state(Session.session_id)
        await state.update_data(session_id=session_id)
        if telegram_user_item['role'] == 'клиент':
            markup = await markups.get_user_main_keyboard_markup()
        elif telegram_user_item['role'] == 'администратор':
            markup = await markups.get_admin_main_keyboard_markup()
        elif telegram_user_item['role'] == 'консультант':
            markup = await markups.get_consultant_keyboard_markup()
        elif telegram_user_item['role'] == 'аналитик':
            markup = await markups.get_analyst_keyboard_markup()
        await message.answer(text=text_samples.session_create_success, parse_mode='HTML',
                             reply_markup=markup)
    except:
        await message.answer(text=text_samples.session_create_error, parse_mode='HTML')

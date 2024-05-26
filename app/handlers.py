from aiogram import types, F, Router, Bot
from aiogram.filters import CommandStart, Command
from app import markups
from aiogram.fsm.context import FSMContext
from database import server_db, object_storage, bank_db
from aiogram.types import Message, FSInputFile, BufferedInputFile
from assets import adaptive_text, text_samples
from app.fsm import NextStep, Session
from app import functions
from analysis import reports

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(text=await adaptive_text.hello_text(message.from_user.username), parse_mode='HTML'
                         )
    await state.set_state(NextStep.password)


@router.message(Command('help'))
async def cmd_start(message: types.Message):
    await message.answer(text='Помощь', parse_mode='HTML')


@router.message(F.text == text_samples.consulting, Session.session_id)
async def cmd_start(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    session_id = state_data.get('session_id')
    await message.answer(text_samples.report_creation_started)
    session_item = await server_db.get_session_item(int(session_id))
    telegram_user_item = await server_db.get_telegram_user_item(session_item['telegram_user_id'])
    report = await server_db.create_report(session_id)
    await reports.create_account_financial_consulting_report(telegram_user_item['account_id'], report['report_id'])
    pdf_report = await object_storage.get_report(report['report_id'])
    await message.answer_document(document=BufferedInputFile(file=pdf_report,
                                                             filename=f'Финансовая консультация {report["report_id"]}.pdf'))


@router.message(NextStep.password)
async def password_check(message: Message, state: FSMContext, bot_object: Bot):
    print('works register')
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

        await message.answer(text=text_samples.password_success, parse_mode='HTML',
                             reply_markup=await markups.get_user_main_keyboard_markup())
        await state.clear()
        await create_session(message, state, server_user_item['telegram_user_id'])
    except:
        await message.reply(text=text_samples.password_error, parse_mode='HTML')


async def create_session(message: Message, state: FSMContext, telegram_user_id: int):
    try:
        moscow_time = await functions.get_message_moscow_time(message.date)
        session_id = await server_db.create_session(telegram_user_id, moscow_time)
        await state.set_state(Session.session_id)
        await state.update_data(session_id=session_id)
        await message.answer(text=text_samples.session_create_success, parse_mode='HTML')
    except Exception as e:
        await message.answer(text=text_samples.session_create_error + '\n' + str(e), parse_mode='HTML')

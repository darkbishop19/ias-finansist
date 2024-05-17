from aiogram import types, F, Router, Bot
from aiogram.filters import CommandStart, Command
from app import markups
from aiogram.fsm.context import FSMContext
from database import server_db
from aiogram.types import Message
from assets import adaptive_text, text_samples
from app.fsm import NextStep

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(text=await adaptive_text.hello_text(message.from_user.username), parse_mode='HTML'
                         )
    await state.set_state(NextStep.password)


@router.message(Command('help'))
async def cmd_start(message: types.Message):
    await message.answer(text='Помощь', parse_mode='HTML')


@router.message(F.text == 'НИКИТА')
async def cmd_start(message: types.Message):
    await message.answer(text=message.text, parse_mode='HTML')


@router.message(NextStep.password)
async def password_check(message: Message, state: FSMContext, bot_object: Bot):
    try:
        server_user_item = await server_db.check_password(message.text)

        if server_user_item['telegram_id'] is not None and server_user_item['telegram_id'] != message.from_user.id:
            print(message.date)
            await bot_object.send_message(chat_id=server_user_item['telegram_id'],
                                          text=await adaptive_text.user_info_changed(message.from_user.id,
                                                                                     message.date))
        elif server_user_item['telegram_id'] is None:
            await server_db.update_user_info(message.text, message.from_user.id, message.from_user.language_code,
                                             message.from_user.username)

        await message.answer(text=text_samples.password_success, parse_mode='HTML')
        await state.clear()
    except Exception as e:
        await message.reply(text=text_samples.password_error + '\n' + str(e), parse_mode='HTML')


@router.message(F.text)
async def reply_mes(message: types.Message):
    await message.reply(text=message.text + '\n' + f'Ваш ID: <code>{message.from_user.id}</code>', parse_mode='HTML')

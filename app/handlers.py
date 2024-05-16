from aiogram import types, F, Router
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
    await message.answer(text=await adaptive_text.hello_text(message.from_user.username), parse_mode='HTML',
                         reply_markup=await markups.get_user_main_keyboard_markup(),
                         )
    await state.set_state(NextStep.password)


@router.message(NextStep.password)
async def password_check(message: Message, state: FSMContext):
    print(f'message:{message.text}')
    try:
        server_user_item = await server_db.check_password(int(message.text))
        print(server_user_item)
        await state.clear()
    except:
        await message.reply(text = text_samples.password_error)



@router.message(Command('help'))
async def cmd_start(message: types.Message):
    await message.answer(text='Помощь', parse_mode='HTML')


@router.message(F.text == 'НИКИТА')
async def cmd_start(message: types.Message):
    await message.answer(text=message.text, parse_mode='HTML')


@router.message(F.text)
async def reply_mes(message: types.Message):
    await message.reply(text=message.text + '\n' + f'Ваш ID: <code>{message.from_user.id}</code>', parse_mode='HTML')

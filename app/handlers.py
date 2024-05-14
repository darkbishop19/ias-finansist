from aiogram import types, F, Router
from aiogram.filters import CommandStart, Command
from app import markups

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(text='Привет' + f"Username: {message.from_user.username}", parse_mode='HTML',
                         reply_markup=await markups.get_user_main_keyboard_markup(),
                         )


@router.message(Command('help'))
async def cmd_start(message: types.Message):
    await message.answer(text='Помощь', parse_mode='HTML')


@router.message(F.text == 'НИКИТА')
async def cmd_start(message: types.Message):
    await message.answer(text=message.text, parse_mode='HTML')


@router.message(F.text)
async def reply_mes(message: types.Message):
    await message.reply(text=message.text + '\n' + f'Ваш ID: <code>{message.from_user.id}</code>', parse_mode='HTML')



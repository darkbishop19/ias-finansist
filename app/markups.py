from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_user_main_keyboard_markup():
    builder = InlineKeyboardBuilder()
    button_hi = InlineKeyboardButton(text='Привет', callback_data='user_hi')
    builder.add(button_hi)
    return builder.as_markup()

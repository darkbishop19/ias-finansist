from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app import text_samples


async def get_user_main_keyboard_markup():
    builder = InlineKeyboardBuilder()
    button_hi = InlineKeyboardButton(text='Привет', callback_data='user_hi')
    builder.add(button_hi)
    return builder.as_markup()

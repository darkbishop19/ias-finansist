from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


async def get_user_main_keyboard_markup():
    builder = ReplyKeyboardBuilder()
    button_profile = KeyboardButton(text='👤 Профиль')
    button_fincial_report = InlineKeyboardButton(text = )
    builder.row(button_profile)
    return builder.as_markup()


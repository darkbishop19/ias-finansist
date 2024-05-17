from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


async def get_user_main_keyboard_markup():
    builder = ReplyKeyboardBuilder()
    ReplyKeyboardMarkup()
    button_profile = KeyboardButton(text='👤 Профиль')
    # button_fincial_report = InlineKeyboardButton(text = '')
    builder.row(button_profile)
    return builder.as_markup(resize_keyboard = True)


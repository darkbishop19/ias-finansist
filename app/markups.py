from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from assets import text_samples


async def get_user_main_keyboard_markup():
    builder = ReplyKeyboardBuilder()
    button_profile = KeyboardButton(text=text_samples.profile)
    button_consulting = KeyboardButton(text=text_samples.consulting)
    button_reports = KeyboardButton(text=text_samples.reports)
    button_session = KeyboardButton(text=text_samples.sessions)
    button_support = KeyboardButton(text=text_samples.support)
    builder.row(button_consulting)
    builder.row(button_profile, button_reports)
    builder.row(button_session, button_support)
    return builder.as_markup(resize_keyboard=True)

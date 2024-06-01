from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from assets import text_samples
from database import bank_db, server_db


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


async def get_admin_main_keyboard_markup():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=text_samples.check_profile))
    builder.row(KeyboardButton(text=text_samples.check_reports))

    return builder.as_markup(resize_keyboard=True)


async def get_consultant_keyboard_markup():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=text_samples.get_report_for_client))

    return builder.as_markup(resize_keyboard=True)

async def get_analyst_keyboard_markup():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=text_samples.get_metrics))

    return builder.as_markup(resize_keyboard=True)

async def get_user_reports(telegram_user_id):
    builder = InlineKeyboardBuilder()
    user_reports = []
    session_items = await server_db.get_user_session_items(telegram_user_id)
    for session in session_items:
        reports = await server_db.get_session_report_items(session["session_id"])
        if len(reports) != 0:
            user_reports.append(reports)
    for item in user_reports:
        for record in item:
            button_report = InlineKeyboardButton(text=f'📊 Отчет_{record["report_id"]}',
                                                 callback_data=f'showreport_{record["report_id"]}')
            builder.row(button_report)

    return builder.as_markup()


async def get_user_sessions(telegram_user_id):
    builder = InlineKeyboardBuilder()
    session_items = await server_db.get_user_session_items(telegram_user_id)
    for session in session_items:
        button_session = InlineKeyboardButton(text=f'📖 Сессия_{session["session_id"]}',
                                              callback_data=f'showsession_{session["session_id"]}')
        builder.row(button_session)
    return builder.as_markup()


async def change_role(telegram_user_id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text_samples.change_role,
                                     callback_data=f'changerole_{telegram_user_id}'))
    return builder.as_markup()


async def choose_role(telegram_user_id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Клиент',
                                     callback_data=f'makeclient_{telegram_user_id}'))
    builder.row(InlineKeyboardButton(text='Аналитик',
                                     callback_data=f'makeanalyst_{telegram_user_id}'))
    builder.row(InlineKeyboardButton(text='Консультант',
                                     callback_data=f'makeconsult_{telegram_user_id}'))
    builder.row(InlineKeyboardButton(text='Администратор',
                                     callback_data=f'makeadmin_{telegram_user_id}'))

    return builder.as_markup()

from datetime import datetime
import datetime
async def hello_text(username):
    if username is None:
        text = f'Здравствуйте !\n' \
               f'Введите ваш пароль ниже:'
    else:
        text = f'Здравствуйте, {username} !\n' \
               f'Введите ваш пароль ниже:'
    return text


async def user_info_changed(telegram_id, time):
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    text = f'В ваш аккаунт вошли !\n' \
           f'ID пользователя в Telegram: {telegram_id}\n' \
           f'Время: {formatted_time} MSK\n\n' \
           f'Вы можете поменять свой пароль: /changepas'
    return text
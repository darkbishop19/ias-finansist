from app import functions


async def hello_text(username):
    if username is None:
        text = f'Здравствуйте !\n' \
               f'Введите ваш пароль ниже:'
    else:
        text = f'Здравствуйте, {username} !\n' \
               f'Введите ваш пароль ниже:'
    return text


async def user_info_changed(telegram_id, username, time):
    moscow_time = await functions.get_message_moscow_time(time)
    formatted_time = moscow_time.strftime("%Y-%m-%d %H:%M:%S")
    text = f'В ваш аккаунт вошли !\n' \
           f'ID пользователя в Telegram: <code>{telegram_id}</code>\n' \
           f'Username пользователя в Telegram: <code>{username}</code>\n' \
           f'Время: {formatted_time} MSK\n\n' \
           f'Вы можете поменять свой пароль: /changepas'
    return text

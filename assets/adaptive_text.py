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


async def get_loans_final_pay(total_needed_sum_to_pay, necessary_sum_to_pay, not_needed_sum_to_pay):
    text = (f'Общая сумма к оплате в этом месяце: {total_needed_sum_to_pay}<br/>'
            f'Обязательная сумма к оплате в этом месяце: {necessary_sum_to_pay}<br/>'
            f'Необязательная сумма к оплате в этом месяце: {not_needed_sum_to_pay}')
    return text

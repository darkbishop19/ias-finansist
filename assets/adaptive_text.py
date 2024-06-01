from app import functions
from database import bank_db, server_db, object_storage


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


async def get_profile_info(telegram_user_id):
    telegram_user_item = await server_db.get_telegram_user_item(telegram_user_id)
    account_item = await bank_db.get_account_item(telegram_user_item['account_id'])
    customer_item = await bank_db.get_customer_item(account_item['customer_id'])
    text = f'Идентификатор: <code>{telegram_user_item["account_id"]}</code>\n' \
           f'Telegram идентификатор: <code>{telegram_user_item["telegram_id"]}</code>\n' \
           f'Telegram имя: <code>{telegram_user_item["username"]}</code>\n' \
           f'ФИО: <code>{customer_item["full_name"]}</code>\n' \
           f'E-mail: <code>{customer_item["mail"]}</code>\n' \
           f'Дата рождения: <code>{customer_item["birth_date"]}</code>\n' \
           f'Свободная сумма на балансе: <code>{account_item["available_balance"] // 1}</code> рублей'
    return text


async def get_all_users_info(telegram_user_id):
    telegram_user_item = await server_db.get_telegram_user_item(telegram_user_id)
    text = ''
    if telegram_user_item['role'] == 'клиент':
        account_item = await bank_db.get_account_item(telegram_user_item['account_id'])
        customer_item = await bank_db.get_customer_item(account_item['customer_id'])
        text = f'Идентификатор: <code>{telegram_user_item["account_id"]}</code>\n' \
               f'Telegram идентификатор: <code>{telegram_user_item["telegram_id"]}</code>\n' \
               f'Telegram имя: <code>{telegram_user_item["username"]}</code>\n' \
               f'ФИО: <code>{customer_item["full_name"]}</code>\n' \
               f'E-mail: <code>{customer_item["mail"]}</code>\n' \
               f'Дата рождения: <code>{customer_item["birth_date"]}</code>\n' \
               f'Свободная сумма на балансе: <code>{account_item["available_balance"] // 1}</code> рублей\n' \
               f'Роль: <code>{telegram_user_item["role"]}</code>'
    elif telegram_user_item['role'] == 'аналитик' or 'консультант':
        text = f'Идентификатор: <code>{telegram_user_item["account_id"]}</code>\n' \
               f'Telegram идентификатор: <code>{telegram_user_item["telegram_id"]}</code>\n' \
               f'Telegram имя: <code>{telegram_user_item["username"]}</code>\n' \
               f'Роль: <code>{telegram_user_item["role"]}</code>'
    return text
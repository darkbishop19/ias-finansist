
async def hello_text(username):
    if username is None:
        text = f'Здравствуйте !\n' \
               f'Введите ваш пароль ниже:'
    else:
        text = f'Здравствуйте, {username} !\n' \
               f'Введите ваш пароль ниже:'
    return text


import datetime

import matplotlib
from asyncpg import Record
from matplotlib import pyplot as plt

from database import bank_db, object_storage


async def get_account_deposit_dataset(account_id, report_id):
    account_deposits = await bank_db.get_account_deposits(account_id)
    deposit_invoices = []
    for deposit in account_deposits:
        deposit_invoices.append(await bank_db.get_deposit_invoices(deposit['deposit_id']))

    future_invoices = await get_future_deposit_invoices(deposit_invoices)
    deposit_list = await check_options_for_deposit_products(future_invoices)
    await create_account_deposit_charts(deposit_invoices, future_invoices, report_id)
    return deposit_list


async def get_future_deposit_invoices(deposit_invoices):
    future_invoices = [record for sublist in deposit_invoices for record in sublist if record['status'] == 'будущий']
    sorted_invoices = sorted(future_invoices, key=lambda x: x['date'])
    return sorted_invoices


async def check_options_for_deposit_products(future_deposit_invoice):
    deposit_descriptions = ['Количество ваших будущих доходов по сберегательной продукции:']
    total_income = 0

    for future_invoice in future_deposit_invoice:
        total_income += future_invoice['payment']
        deposit = await bank_db.get_deposit_item(future_invoice['deposit_id'])
        deposit_product = await bank_db.get_deposit_product_item(deposit['deposit_product_id'])
        deposit_type = await bank_db.get_deposit_type_item(deposit_product['deposit_type_id'])

        deposit_description = (f'ID платежа: {future_invoice["deposit_invoice_id"]}<br/>'
                               f'Название продукта: {deposit_product["name"]}<br/>'
                               f'Дата: {future_invoice["date"]}<br/>'
                               f'Сумма начисления: {future_invoice["payment"]} рублей<br/>'
                               f'Сумма счета на текущий момент: {future_invoice["current_amount"]} рублей<br/>')
        deposit_privileges = 'Льготы: '
        if deposit_type['min_amount_for_bonus'] is not None and deposit['current_amount'] > deposit_type[
            'min_amount_for_bonus']:
            deposit_privileges += f'На вашем продукте {deposit["product_name"]} активирована бонусная процентная ставка: {deposit_type["bonus_rate"]}.' \
                                  f'Для сохранение бонуса, баланс счета не должен упасть ниже: {deposit_type["min_amount_for_bonus"]}'
        else:
            deposit_privileges += 'Нет'
        deposit_description += deposit_privileges
        deposit_descriptions.append(deposit_description)

    deposit_list = {
        'deposit_descriptions': deposit_descriptions,
        'deposits_total_income': total_income,
    }

    return deposit_list


async def create_deposit_advice(account_id, necessary_sum_to_pay):
    account_item = await bank_db.get_account_item(account_id)
    available_balance = account_item['available_balance'] - necessary_sum_to_pay
    if available_balance < 0:
        available_balance = 0
    user_deposits = await bank_db.get_account_deposits(account_id)
    existing_future_invoices_income = 0
    for deposit in user_deposits:
        deposit_invoices = await bank_db.get_deposit_invoices(deposit['deposit_id'])
        for invoice in deposit_invoices:
            if invoice['status'] == 'будущий':
                existing_future_invoices_income += invoice['payment']
    account_deposit_product_ids = [user_deposit['deposit_product_id'] for user_deposit in user_deposits]
    max_user_rate = 0
    user_best_product = Record
    for product_id in account_deposit_product_ids:
        deposit_product_item = await bank_db.get_deposit_product_item(product_id)
        if deposit_product_item['rate'] > max_user_rate:
            max_user_rate = deposit_product_item['rate']
            user_best_product = deposit_product_item
    changed = False
    bonus_rate_needed = False
    promising_product = Record
    bank_deposit_products = await bank_db.get_all_bank_deposit_products()
    for product in bank_deposit_products:
        product_type = await bank_db.get_deposit_type_item(product['deposit_type_id'])
        if product['rate'] > max_user_rate and product['limit_min'] < available_balance:
            max_user_rate = product['rate']
            changed = True
        if product_type['bonus_rate'] is not None and product_type['bonus_rate'] > max_user_rate and \
                product_type['min_amount_for_bonus'] <= available_balance and product['limit_min'] < available_balance:
            max_user_rate = product['rate']
            changed = True
            bonus_rate_needed = True
            promising_product = product
    if bonus_rate_needed and changed:
        product_type = await bank_db.get_deposit_type_item(promising_product['deposit_type_id'])
        advice = [(f'Советуем открыть: {promising_product["name"]}.<br/>'
                   f'Сейчас в банке действует акция: при депозите в данный продукт '
                   f'суммы от {product_type["min_amount_for_bonus"] // 1} рублей процентная ставка увеличивается до {product_type["bonus_rate"] * 100} %.<br/>'
                   f'Ваш свободный баланс после уплаты расходов по кредитной продукции: {available_balance} рублей удовлетворяет условиям акции.')]
        advice.append(f'Ваш итоговый доход за месяц по рекомендации: {available_balance*product_type["bonus_rate"]/12 + existing_future_invoices_income} рублей<br/>'
                      f'Ваш итоговый доход за месяц без рекомендации: {existing_future_invoices_income} рублей')
    elif changed:
        advice = [f'Советуем открыть: {promising_product["name"]}.<br/>' 
                 f'Процентная ставка {promising_product["rate"] * 100} % по продукту принесет вам больше всего выгоды.<br/>' 
                 f'Ваш свободный баланс после уплаты расходов по кредитной продукции: {available_balance} рублей удовлетворяет условиям открытия продукта.']
        advice.append(f'Ваш итоговый доход за месяц: {available_balance*promising_product["rate"]/12 + existing_future_invoices_income} рублей<br/>'
                      f'Ваш итоговый доход за месяц без рекомендации: {existing_future_invoices_income} рублей')
    elif available_balance > 0:
        advice = [f'Советуем вложить средства в открытый продукт: {user_best_product["name"]}<br/>' 
                 f'Ваш свободный баланс после уплаты расходов по кредитной продукции: {available_balance}']
        advice.append(f'Ваш итоговый доход за месяц: {available_balance*user_best_product["rate"]/12 + existing_future_invoices_income} рублей<br/>'
                      f'Ваш итоговый доход за месяц без рекомендации: {existing_future_invoices_income} рублей')

    else:
        advice = [f'На текущий момент для вас выгоднее всего вложить средства в погашение платежей по кредитной продукции.<br/>' 
                 f'Ваш свободный баланс после уплаты расходов по кредитной продукции: {available_balance}']
    return advice


async def create_account_deposit_charts(deposit_invoices, future_invoices, report_id):
    matplotlib.use('Agg')
    data_payments = []
    for invoice_list in deposit_invoices:
        for record in invoice_list:
            data_payments.append({
                'date': record['date'],
                'payment': record['payment'],
                'status': record['status'],
                'deposit_id': record['deposit_id']
            })
    data_payments.sort(key=lambda x: x['date'])
    last_10_data_invoices = data_payments[-10:]
    last_10_payments = []
    last_future_payments = []
    future_dates = []
    for invoice in last_10_data_invoices:
        value = invoice['payment']

        for item in last_10_payments:
            if item['date'] == invoice['date']:
                value += item['payment']
        last_10_payments.append({
            'date': invoice['date'],
            'payment': value
        })

    for future_invoice in last_10_data_invoices:
        if future_invoice['status'] == 'будущий':
            value = future_invoice['payment']

            for item in last_future_payments:
                if item['date'] == future_invoice['date']:
                    value += item['payment']

            last_future_payments.append({
                'date': future_invoice['date'],
                'payment': value
            })

    last_10_payments_dates = [item['date'] for item in last_10_payments]
    last_10_payments_payments = [item['payment'] for item in last_10_payments]
    last_future_payments_dates = [item['date'] for item in last_future_payments]
    last_future_payments_payments = [item['payment'] for item in last_future_payments]
    plt.figure(figsize=(16, 10))
    plt.bar(last_10_payments_dates, last_10_payments_payments, color='red', label='Прошлый совокупный доход', width=1)
    plt.bar(last_future_payments_dates, last_future_payments_payments, color='green', label='Будущий совокупный доход',
            width=1)
    plt.xlabel('Дата', fontsize=16)
    plt.ylabel('Сумма платежа', fontsize=16)
    plt.title('Платежи по сберегательным продуктам', fontsize=16)
    plt.xticks(last_10_payments_dates, rotation=45)
    plt.legend()
    plt.savefig('analysis/deposit_chart.png')
    plt.close()
    await object_storage.add_deposit_chart(report_id)

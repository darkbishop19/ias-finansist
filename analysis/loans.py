import datetime

from database import bank_db, object_storage
import matplotlib.pyplot as plt
import matplotlib
from datetime import timedelta, datetime, date


async def get_account_loan_dataset(account_id, report_id):
    account_loans = await bank_db.get_account_loans(account_id)
    loan_invoices = []
    for loan in account_loans:
        loan_invoices.append(await bank_db.get_account_loan_payments(loan['loan_id']))
    future_invoices = await get_future_loan_invoices(loan_invoices)

    options_text = await check_options_for_loan_products(future_invoices)
    await create_account_loans_charts(loan_invoices, report_id)
    return options_text


async def get_future_loan_invoices(loan_invoices):
    future_invoices = [record for sublist in loan_invoices for record in sublist if record['status'] == 'будущий']
    sorted_invoices = sorted(future_invoices, key=lambda x: x['date'])
    return sorted_invoices


async def check_options_for_loan_products(future_loan_invoice):
    options_for_loans = 'Количество ваших будущих платежей по кредитной продукции:\n\n'
    total_needed_sum_to_pay = 0
    not_needed_sum_to_pay = 0
    for future_invoice in future_loan_invoice:
        total_needed_sum_to_pay += future_invoice['payment']
        loan = await bank_db.get_loan_item(future_invoice['loan_id'])
        loan_product = await bank_db.get_loan_product(loan['loan_product_id'])
        loan_type = await bank_db.get_loan_type(loan_product['loan_type_id'])

        options_for_loans += f'ID платежа: {future_invoice["loan_invoice_id"]}\n' \
                             f'Название продукта: {loan_product["name"]}\n' \
                             f'Дата: {future_invoice["date"]}\n' \
                             f'Платеж: {future_invoice["payment"]}\n' \
                             f'Сумма покрытия тела долга: {future_invoice["body_amount"]}\n' \
                             f'Сумма покрытия начисленного долга: {future_invoice["payment"] - future_invoice["body_amount"]}\n'

        time_difference = future_invoice['date'] - loan['create_date']
        time_difference_months = time_difference.days / 30.44
        privileges = 'Льготы:'
        if loan_type['grace_period_months'] is not None and time_difference_months < loan_type['grace_period_months']:
            privileges += 'Льготный период. Дополнительные проценты и штрафы не начисляются.'
            not_needed_sum_to_pay += future_invoice['payment']
        else:
            privileges += 'Нет'
        options_for_loans += privileges + '\n\n'
    necessary_sum_to_pay = total_needed_sum_to_pay - not_needed_sum_to_pay
    options_to_pay = f'Общая сумма к оплате в этом месяце: {total_needed_sum_to_pay}\n' \
                     f'Обязательная сумма к оплате в этом месяце: {necessary_sum_to_pay}\n' \
                     f'Необязательная сумма к оплате в этом месяце: {not_needed_sum_to_pay}'
    options_for_loans += '\n' + options_to_pay
    return options_for_loans


async def create_account_loans_charts(loan_invoices, report_id):
    matplotlib.use('Agg')
    data_payments = []
    body_payments = []
    past_payments = []
    for invoice_list in loan_invoices:
        for record in invoice_list:
            data_payments.append((record['date'], record['payment']))
            body_payments.append((record['date'], record['body_amount']))
            if record['status'] == 'оплачен':
                past_payments.append((record['date'], record['payment']))
    data_payments.sort(key=lambda x: x[0])
    body_payments.sort(key=lambda x: x[0])
    dates = [date for date, _ in data_payments]
    payments = [payment for _, payment in data_payments]
    body_amounts = [body_amount for _, body_amount in body_payments]
    past_dates = [date for date, _ in past_payments]
    past_payments = [payment for _, payment in past_payments]
    plt.figure(figsize=(16, 10))
    plt.bar(dates, payments, color='blue', label='Платеж')
    plt.bar(dates, body_amounts, color='green', label='Сумма покрытия тела долга')
    plt.bar(past_dates, past_payments, color='red', label='Прошлые платежи')

    plt.xlabel('Дата', fontsize=16)
    plt.ylabel('Сумма платежа', fontsize=16)
    plt.title('Платежи по кредитам', fontsize=16)
    plt.xticks(dates)
    plt.legend()
    plt.savefig('analysis/loan_chart.png')
    plt.close()
    await object_storage.add_loan_chart(report_id)

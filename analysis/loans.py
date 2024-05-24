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

    loans_list = await check_options_for_loan_products(future_invoices)
    await create_account_loans_charts(loan_invoices, report_id)
    return loans_list


async def get_future_loan_invoices(loan_invoices):
    future_invoices = [record for sublist in loan_invoices for record in sublist if record['status'] == 'будущий']
    sorted_invoices = sorted(future_invoices, key=lambda x: x['date'])
    return sorted_invoices


async def check_options_for_loan_products(future_loan_invoice):
    loans_description = ['Количество ваших будущих платежей по кредитной продукции:']
    loans_advice = []
    total_needed_sum_to_pay = 0
    not_needed_sum_to_pay = 0

    for future_invoice in future_loan_invoice:
        total_needed_sum_to_pay += future_invoice['payment']
        loan = await bank_db.get_loan_item(future_invoice['loan_id'])
        loan_product = await bank_db.get_loan_product(loan['loan_product_id'])
        loan_type = await bank_db.get_loan_type(loan_product['loan_type_id'])

        loan_description = (f'ID платежа: {future_invoice["loan_invoice_id"]}<br/>'
                            f'Название продукта: {loan_product["name"]}<br/>'
                            f'Дата: {future_invoice["date"]}<br/>'
                            f'Сумма платежа: {future_invoice["payment"]}<br/>'
                            f'Сумма покрытия тела долга: {future_invoice["body_amount"]}<br/>'
                            f'Сумма покрытия процентов начисленного долга: {future_invoice["payment"] - future_invoice["body_amount"]}<br/>')

        time_difference = future_invoice['date'] - loan['create_date']
        time_difference_months = time_difference.days / 30.44
        loan_privilege = 'Льготы: '
        if loan_type['grace_period_months'] is not None and time_difference_months < loan_type['grace_period_months']:
            loan_privilege += 'Льготный период. Дополнительные проценты и штрафы не начисляются.'
            not_needed_sum_to_pay += future_invoice['payment']
            loans_advice.append(
                f'Советуем сэкономить в этом месяце на оплате платежа по продукту:<b> {loan_product["name"]}</b>.<br/>'
                f'Размер экономии:<b> {future_invoice["payment"]} рублей.</b><br/> '
                f'Для получения дополнительного дохода вложите средства в сберегательные продукты банка.<br/><br/>')

        else:
            loan_privilege += 'Нет'
        loan_description += loan_privilege
        loans_description.append(loan_description)
    necessary_sum_to_pay = total_needed_sum_to_pay - not_needed_sum_to_pay
    loans_list = {
        'loans_description': loans_description,
        'loans_advice': loans_advice,
        'necessary_sum_to_pay': necessary_sum_to_pay,
        'total_needed_sum_to_pay': total_needed_sum_to_pay,
        'not_needed_sum_to_pay': not_needed_sum_to_pay
    }
    return loans_list


async def create_account_loans_charts(loan_invoices, report_id):
    matplotlib.use('Agg')
    data_payments = []
    body_payments = []
    past_payments = []
    for invoice_list in loan_invoices:
        for record in invoice_list:
            data_payments.append({'date': record['date'],
                                  'payment': record['payment'],
                                  'body_payment': record['body_amount'],
                                  'status': record['status']})
    data_payments.sort(key=lambda x: x['date'])
    last_10_data_payments = data_payments[-10:]
    last_10_payments = []
    last_future_payments = []
    for invoice in last_10_data_payments:
        value = invoice['payment']
        body_value = invoice['body_payment']
        for each in last_10_payments:
            if each['date'] == invoice['date']:
                value += each['payment']
                body_value += each['body_payment']
        last_10_payments.append(
            {
                'date': invoice['date'],
                'payment': value,
                'body_payment': body_value
            }
        )
        if invoice['status'] == 'будущий':
            future_value = invoice['payment']
            future_body_value = invoice['body_payment']
            for each_future in last_future_payments:
                if each_future['date'] == invoice['date']:
                    future_value += each_future['payment']
                    future_body_value += each_future['body_payment']
            last_future_payments.append({
                'date': invoice['date'],
                'payment': future_value,
                'body_payment': body_value
            })
    last_payments_payments = [item['payment'] for item in last_10_payments]
    last_payments_dates = [item['date'] for item in last_10_payments]
    last_payments_body_payments = [item['body_payment'] for item in last_10_payments]
    future_payments_payments = [item['payment'] for item in last_future_payments]
    future_payments_dates = [item['date'] for item in last_future_payments]
    future_payments_body_payments = [item['body_payment'] for item in last_future_payments]
    plt.figure(figsize=(16, 10))
    plt.bar(last_payments_dates, last_payments_payments, color='red', label='Общая сумма платежа')
    plt.bar(last_payments_dates, last_payments_body_payments, color='orange', label='Общая сумма покрытия тела долга')
    plt.bar(future_payments_dates, future_payments_payments, color='green', label='Общая сумма будущего платежа')
    plt.bar(future_payments_dates, future_payments_body_payments, color='blue',
            label='Общая сумма будущего покрытия тела долга')
    plt.xlabel('Дата', fontsize=16)
    plt.ylabel('Сумма платежа', fontsize=16)
    plt.title('Платежи по кредитам', fontsize=16)
    plt.xticks(last_payments_dates, rotation=45)
    plt.legend()
    plt.savefig('analysis/loan_chart.png')
    plt.close()
    await object_storage.add_loan_chart(report_id)

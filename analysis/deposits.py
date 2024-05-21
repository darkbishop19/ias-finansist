import matplotlib
from matplotlib import pyplot as plt

from database import bank_db, object_storage


async def get_account_deposit_dataset(account_id, report_id):
    account_deposits = await bank_db.get_account_deposits(account_id)
    deposit_invoices = []
    for deposit in account_deposits:
        deposit_invoices.append(await bank_db.get_deposit_invoices(deposit['deposit_id']))

    future_invoices = await get_future_deposit_invoices(deposit_invoices)
    print(future_invoices)
    options_text = await check_options_for_deposit_products(future_invoices)
    await create_account_deposit_charts(deposit_invoices, report_id)
    return options_text


async def get_future_deposit_invoices(deposit_invoices):
    future_invoices = [record for sublist in deposit_invoices for record in sublist if record['status'] == 'будущий']
    sorted_invoices = sorted(future_invoices, key=lambda x: x['date'])
    return sorted_invoices


async def check_options_for_deposit_products(future_deposit_invoice):
    options_for_deposits = 'Количество ваших будущих доходов по сберегательной продукции:\n\n'
    total_needed_sum_to_pay = 0
    not_needed_sum_to_pay = 0
    for future_invoice in future_deposit_invoice:
        deposit = await bank_db.get_deposit_item(future_invoice['deposit_id'])
        deposit_product = await bank_db.get_deposit_product_item(deposit['deposit_product_id'])
        deposit_type = await bank_db.get_deposit_type_item(deposit_product['deposit_type_id'])

        options_for_deposits += f'ID платежа: {future_invoice["deposit_invoice_id"]}\n' \
                                f'Название продукта: {deposit_product["name"]}\n' \
                                f'Дата: {future_invoice["date"]}\n' \
                                f'Сумма начисления: {future_invoice["payment"]} рублей\n' \
                                f'Сумма счета: {future_invoice["current_amount"]} рублей\n'

        # time_difference = future_invoice['date'] - deposit['create_date']
        # time_difference_months = time_difference.days / 30.44
        privileges = 'Льготы:'
        options_for_deposits += privileges + '\n\n'
    necessary_sum_to_pay = total_needed_sum_to_pay - not_needed_sum_to_pay
    options_to_pay = f'Общая сумма к оплате в этом месяце: {total_needed_sum_to_pay}\n' \
                     f'Обязательная сумма к оплате в этом месяце: {necessary_sum_to_pay}\n' \
                     f'Необязательная сумма к оплате в этом месяце: {not_needed_sum_to_pay}'
    options_for_deposits += '\n' + options_to_pay
    return options_for_deposits


async def create_account_deposit_charts(deposit_invoices, report_id):
    matplotlib.use('Agg')
    data_payments = []
    past_payments = []
    for invoice_list in deposit_invoices:
        for record in invoice_list:
            data_payments.append((record['date'], record['payment']))
            if record['status'] == 'оплачен':
                past_payments.append((record['date'], record['payment']))
    data_payments.sort(key=lambda x: x[0])
    dates = [date for date, _ in data_payments]
    payments = [payment for _, payment in data_payments]
    past_dates = [date for date, _ in past_payments]
    past_payments = [payment for _, payment in past_payments]
    plt.figure(figsize=(16, 10))
    plt.plot(dates, payments, color='blue', label='Сумма дохода')
    plt.plot(past_dates, past_payments, color='red', label='Прошлые платежи')

    plt.xlabel('Дата', fontsize=16)
    plt.ylabel('Сумма платежа', fontsize=16)
    plt.title('Платежи по сберегательным продуктам', fontsize=16)
    plt.xticks(dates)
    plt.legend()
    plt.savefig('analysis/deposit_chart.png')
    plt.close()
    await object_storage.add_loan_chart(report_id)

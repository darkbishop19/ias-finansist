from database import bank_db
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.dates import DateFormatter, DayLocator
from collections import defaultdict
from analysis import loans


async def get_account_advices_data(account_id, report_id):
    loan_options_text = await loans.get_account_loan_dataset(account_id, report_id)

    return loan_options_text




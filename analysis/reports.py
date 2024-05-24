import io
from collections import defaultdict
from database import object_storage
from reportlab.lib.utils import ImageReader

from analysis import loans, deposits
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from assets import adaptive_text, text_samples


async def get_account_advices_data(account_id, report_id):
    print('work')
    loans_list = await loans.get_account_loan_dataset(account_id, report_id)
    loans_pay_final = await adaptive_text.get_loans_final_pay(loans_list['total_needed_sum_to_pay'],
                                                              loans_list['necessary_sum_to_pay'],
                                                              loans_list['not_needed_sum_to_pay'])
    deposit_advice = await deposits.create_deposit_advice(account_id, loans_list['necessary_sum_to_pay'])
    deposit_list = await deposits.get_account_deposit_dataset(account_id, report_id)
    deposits_total_income_text = f'Общая сумма дохода по вашим дебетовым продуктам: {deposit_list["deposits_total_income"]} рублей.'
    await generate_pdf_report(loans_list['loans_advice'], loans_list['loans_description'], loans_pay_final,
                              deposit_list['deposit_descriptions'], deposits_total_income_text,
                              deposit_advice,
                              report_id)
    print('done')
    return ''


async def generate_pdf_report(loans_advice, loans_description, loans_pay_final,
                              deposits_description, deposits_total_income, deposit_advice,
                              report_id):
    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))
    doc = SimpleDocTemplate(
        "analysis/report.pdf",
        pagesize=A4,
        encoding='UTF-8',
        title='Отчет "Финансовая консультация"'
    )

    Story = []

    # Create styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='RussianNormal', parent=styles['Normal'], fontName='TimesNewRoman', fontSize=12))
    styles.add(ParagraphStyle(name='CustomTitle', parent=styles['Normal'], fontName='TimesNewRoman', fontSize=20,
                              spaceAfter=20, alignment=1))
    styles.add(ParagraphStyle(name='SectionTitle', parent=styles['Normal'], fontName='TimesNewRoman', fontSize=16,
                              spaceAfter=20, alignment=1, bold=1))
    title_text = 'Отчет "Финансовая консультация"'
    Story.append(Paragraph(title_text, styles['CustomTitle']))
    Story.append(Spacer(1, 12))

    # Add text to the document
    for text in loans_description:
        Story.append(Paragraph(text, styles['RussianNormal']))
        Story.append(Spacer(1, 10))
    Story.append(Spacer(1, 10))
    print(loans_pay_final)
    Story.append(Paragraph(loans_pay_final, styles['RussianNormal']))
    Story.append(Spacer(1, 10))

    # Add an image to the document
    image_bytes = await object_storage.get_loan_chart(report_id)
    memory_file = io.BytesIO(image_bytes)
    Story.append(Image(memory_file, width=456, height=300))
    # Build the PDF
    Story.append(Spacer(1, 10))

    for text in deposits_description:
        Story.append(Paragraph(text, styles['RussianNormal']))
        Story.append(Spacer(1, 10))

    Story.append(Spacer(1, 10))
    Story.append(Paragraph(deposits_total_income, styles['RussianNormal']))
    Story.append(Spacer(1, 10))

    Story.append(Spacer(1, 10))
    image_bytes = await object_storage.get_loan_chart(report_id)
    memory_file = io.BytesIO(image_bytes)
    Story.append(Image(memory_file, width=456, height=300))
    Story.append(Spacer(1, 10))
    for text in loans_advice:
        Story.append(Paragraph(text, styles['RussianNormal']))
    Story.append(Spacer(1, 10))
    Story.append(Paragraph(deposit_advice, styles['RussianNormal']))

    doc.build(Story)
    await object_storage.add_report(report_id)

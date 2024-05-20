
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Предположим, что у вас есть текст и изображение
text = f'Общая сумма к оплате в этом месяце: {1000}\n' \
       f'Обязательная сумма к оплате в этом месяце: {1100}\n' \
       f'Необязательная сумма к оплате в этом месяце: {1200}'



# Создание документа PDF
doc = SimpleDocTemplate("report.pdf", pagesize=A4,
                        encoding='UTF-8',
                        title = 'Отчет "Финансовая консультация клиента".')
pdfmetrics.registerFont(TTFont('arial', 'arial.ttf'))

Story = []
# Создание стилей
styles = getSampleStyleSheet()

styleN = styles['Normal'].fontName='Geist-Light'
styleH = styles['Heading1']

# Добавление текста в документ
text_elements = []
Story.append(Paragraph(text, styleN))

# Добавление изображения в документ

Story.append(Image('loan_chart.png', width=456, height=300))
# Создание PDF
doc.build(Story)
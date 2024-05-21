from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch

# Register the font
pdfmetrics.registerFont(TTFont('TimesNewRoman', 'Times New Roman.ttf'))

# Create a sample text
text = (
    f'<br/>Общая сумма к оплате в этом месяце: {1000}'
    f'<br/>Обязательная сумма к оплате в этом месяце: {100}'
    f'<br/>Необязательная сумма к оплате в этом месяце: 1200'
)

# Create a PDF document
doc = SimpleDocTemplate(
    "report.pdf",
    pagesize=A4,
    encoding='UTF-8',
    title='Отчет "Финансовая консультация клиента".'
)

# Create a story list
Story = []

# Create styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='RussianNormal', parent=styles['Normal'], fontName='TimesNewRoman', fontSize=12))

# Add text to the document
Story.append(Paragraph(text, styles['RussianNormal']))
Story.append(Spacer(1, 20))

# Add an image to the document
Story.append(Image('loan_chart.png', width=456, height=300))

# Build the PDF
doc.build(Story)

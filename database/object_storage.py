import io
import os

import boto3
from dotenv import load_dotenv
from matplotlib import image as mpimg

load_dotenv()
telegram_s3 = boto3.resource(
    's3',
    endpoint_url=os.getenv('s3_endpoint_url'),
    region_name='ru-central1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

bucket = telegram_s3.Bucket(os.getenv('bucket_name'))


async def add_loan_chart(report_id):
    telegram_s3.Object(os.getenv('bucket_name'), f'charts/loan_{report_id}.png').put(
        Body=open('analysis/loan_chart.png', 'rb'))


async def add_deposit_chart(report_id):
    telegram_s3.Object(os.getenv('bucket_name'), f'charts/deposit_{report_id}.png').put(
        Body=open('analysis/deposit_chart.png', 'rb'))


async def get_loan_chart(report_id):
    object = bucket.Object(f'charts/loan_{report_id}.png')

    img_data = object.get().get('Body').read()

    return img_data


async def get_deposit_chart(report_id):
    object = bucket.Object(f'charts/deposit_{report_id}.png')

    img_data = object.get().get('Body').read()

    return img_data


async def add_report(report_id):
    bucket.upload_file("analysis/report.pdf", f"reports/report_{report_id}.pdf")

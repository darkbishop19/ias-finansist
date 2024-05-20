import io
import os

import boto3
from dotenv import load_dotenv

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
    telegram_s3.Object(os.getenv('bucket_name'), f'charts/loan_{report_id}.png').put(Body=open('database/loan_chart.png', 'rb'))

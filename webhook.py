import requests
from dotenv import load_dotenv
import os
load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
url = "https://api.telegram.org/bot{token}/{method}".format(
    token=bot_token,
      # method="setWebhook"
     # method="getWebhookinfo"
     method="deleteWebhook"
)

function_url = os.getenv('WEBHOOK')
data = {"url": function_url}

r = requests.post(url, data=data)
print(r.json())
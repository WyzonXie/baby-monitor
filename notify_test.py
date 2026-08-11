import requests
from config import WEBHOOK_URL

def send_notification(message):
    payload = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    response = requests.post(WEBHOOK_URL, json=payload)
    return response

response = send_notification("Baby is crying! 宝宝正在哭泣！")
print(response.text)
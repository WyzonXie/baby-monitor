import requests
from config import WEBHOOK_URL

def send_notification(message):
    payload = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload,timeout=5)
    except requests.exceptions.RequestException as e:
        webhook_key = WEBHOOK_URL.split("key=")[-1]
        safe_message = str(e).replace(webhook_key, "***")
        print(f"Error sending notification: {safe_message}")
        return None
    return response
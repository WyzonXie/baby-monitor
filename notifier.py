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
        print(f"Error sending notification: {e}")
        return None
    return response
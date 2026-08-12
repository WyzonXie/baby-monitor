from notifier import send_notification 
response = send_notification("Baby is crying! 宝宝正在哭泣！")
if response is None:
    print("Failed to send notification.")
else:
    print(response.text)
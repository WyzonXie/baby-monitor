from notifier import send_notification 
response = send_notification("Baby is crying! 宝宝正在哭泣！")
print(response.text)
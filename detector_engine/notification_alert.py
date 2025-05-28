import requests
import json

with open("config.json", "r") as f:
    config = json.load(f)

TELEGRAM_BOT_TOKEN = config["telegram_bot_token"]
TELEGRAM_CHAT_ID = config["telegram_chat_id"]

def send_telegram_video(filename):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    with open(filename, 'rb') as video:
        files = {'video': video}
        data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': '🔥 Phát hiện lửa hoặc khói!'}
        requests.post(url, files=files, data=data)

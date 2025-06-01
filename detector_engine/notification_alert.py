import requests
import json
import os

with open("config.json", "r") as f:
    config = json.load(f)

TELEGRAM_BOT_TOKEN = config["telegram_bot_token"]
TELEGRAM_CHAT_ID = config["telegram_chat_id"]

def send_telegram_video(filename):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    with open(filename, 'rb') as video:
        files = {'video': video}
        data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': '🔥 Phát hiện lửa hoặc khói!'}
        try:
            res = requests.post(url, files=files, data=data)
            if res.status_code == 200:
                remove_sent_file()
            else:
                print(f"Request failed with status code: {res.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")


def remove_sent_file():
    folder = 'tmp'
    for filename in os.listdir(folder):
        print(filename)
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                # Nếu trong tmp có folder con, xóa đệ quy (nếu cần)
                import shutil
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error when trying to remove file {file_path}: {e}")
import requests
from bs4 import BeautifulSoup
import time
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)


TOKEN = "8463282045:AAGmCnljPnbU1MEtH4g-Emfap_2qgnBUm_U"
CHAT_ID = "8586986001"
KAFEEL_URL = "https://kafeel.me/projects"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.get(url, params=payload, timeout=10)
    except:
        print("Failed to send message")

def monitor_kafeel():
    last_project = ""
    send_telegram_msg("🚀 Radar is Active!")
    while True:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(KAFEEL_URL, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            first_project = soup.find('h3').text.strip()
            if first_project != last_project:
                if last_project != "":
                    msg = f"🔔 *New Project!*\n\n📌 {first_project}\n\n🔗 [Link]({KAFEEL_URL})"
                    send_telegram_msg(msg)
                last_project = first_project
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)

if __name__ == "__main__":
    t = Thread(target=run_server)
    t.start()
    monitor_kafeel()
import requests
import re
import time
import threading
from flask import Flask

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8699061983:AAFlnNfxuVYV6mZ6qF50Ye2yAUA3daEs0IY"
TELEGRAM_CHAT_ID = "2022031820"
SEARCH_QUERY = "игровой ноутбук"
CITY = "sochi"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except:
        pass

def get_avito_ads():
    url = f"https://www.avito.ru/{CITY}/predlozheniya_uslug?q={SEARCH_QUERY}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    ids = re.findall(r'itemId-(\d+)', response.text)
    ads = []
    for ad_id in ids[:10]:
        ads.append({"id": ad_id, "url": f"https://www.avito.ru/{CITY}/predlozheniya_uslug/{ad_id}"})
    return ads

def run_bot():
    seen = set()
    send_telegram("✅ Бот запущен")
    while True:
        try:
            ads = get_avito_ads()
            for ad in ads:
                if ad["id"] not in seen:
                    seen.add(ad["id"])
                    send_telegram(f"🆕 НОВОЕ ОБЪЯВЛЕНИЕ!\n{ad['url']}")
            time.sleep(60)
        except:
            time.sleep(60)

@app.route('/')
def home():
    return "Bot running"

@app.route('/health')
def health():
    return "OK"

if __name__ == "__main__":
    thread = threading.Thread(target=run_bot)
    thread.start()
    app.run(host="0.0.0.0", port=10000)
import requests
import json
import os
from datetime import datetime

# ---------------- CONFIG ----------------

# Square number range
START = 261
END = 402
STEP = 3

# Price tolerance (USD)
TOLERANCE = 50  

# CoinGecko BTC price API (FREE)
PRICE_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

# Telegram secrets (from GitHub Secrets)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

STATE_FILE = "alerted.json"

# ---------------- HELPERS ----------------

def get_btc_price():
    r = requests.get(PRICE_URL, timeout=10)
    r.raise_for_status()
    data = r.json()
    return float(data["bitcoin"]["usd"])


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, json=payload, timeout=10)


def load_alerted():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_alerted(data):
    with open(STATE_FILE, "w") as f:
        json.dump(list(data), f)

# ---------------- MAIN LOGIC ----------------

def main():
    price = get_btc_price()
    alerted = load_alerted()

    for n in range(START, END + 1, STEP):
        level = n * n

        if abs(price - level) <= TOLERANCE and level not in alerted:
            msg = (
                f"🚨 BTC LEVEL HIT 🚨\n\n"
                f"Square Level: {n} × {n}\n"
                f"Level Price: {level}\n"
                f"BTC Price: {price}\n"
                f"Time: {datetime.utcnow()} UTC"
            )
            send_telegram(msg)
            alerted.add(level)

    save_alerted(alerted)

# ---------------- RUN ----------------

if __name__ == "__main__":
    main()

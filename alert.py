import os
import requests
import math
import json
from datetime import datetime

# --- Telegram credentials from GitHub Secrets ---
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# --- BTC price source (free, no key) ---
PRICE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

# --- Square level settings ---
START = 261
END = 402
STEP = 3
TOLERANCE = 10  # USD range to consider "touched"

# --- File to store already-alerted levels ---
STATE_FILE = "alerted.json"


def get_btc_price():
    r = requests.get(PRICE_URL, timeout=10)
    return float(r.json()["price"])


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, json=payload, timeout=10)


def load_alerted():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, "r") as f:
        return set(json.load(f))


def save_alerted(data):
    with open(STATE_FILE, "w") as f:
        json.dump(list(data), f)


def main():
    price = get_btc_price()
    alerted = load_alerted()

    for n in range(START, END + 1, STEP):
        level = n * n
        if abs(price - level) <= TOLERANCE and level not in alerted:
            msg = (
                f"🚨 BTC LEVEL HIT 🚨\n\n"
                f"Level: {n} × {n} = {level}\n"
                f"Price: {price}\n"
                f"Time: {datetime.utcnow()} UTC"
            )
            send_telegram(msg)
            alerted.add(level)

    save_alerted(alerted)


if __name__ == "__main__":
    main()

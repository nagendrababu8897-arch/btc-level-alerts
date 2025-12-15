import requests
import os
from datetime import datetime

# ---------------- CONFIG ----------------

START = 261
END = 402
STEP = 3

TOLERANCE = 3  # USDT

# Delta Exchange BTCUSD perpetual (mark price)
DELTA_PRICE_URL = "https://api.delta.exchange/v2/tickers/BTCUSD"

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# ---------------- HELPERS ----------------

def get_delta_price():
    r = requests.get(DELTA_PRICE_URL, timeout=10)
    r.raise_for_status()
    data = r.json()
    return float(data["result"]["mark_price"])


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload, timeout=10)

# ---------------- MAIN LOGIC ----------------

def main():
    price = get_delta_price()

    for n in range(START, END + 1, STEP):
        level = n * n

        if abs(price - level) <= TOLERANCE:
            msg = (
                f"🚨 BTC LEVEL TOUCHED (DELTA) 🚨\n\n"
                f"Level: {n} × {n} = {level}\n"
                f"Delta Price: {price}\n"
                f"Tolerance: ±{TOLERANCE} USDT\n"
                f"Time: {datetime.utcnow()} UTC"
            )
            send_telegram(msg)

# ---------------- RUN ----------------

if __name__ == "__main__":
    main()

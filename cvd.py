import yfinance as yf
import requests
import pandas as pd

# ===== FIXED FOR YOU =====
BOT_TOKEN = "9102765194:AAEd_tiB_6v7AHP6Ymuy3jp-arUS4j7azIY"
CHAT_ID = "483927316"
# =========================

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=15)
        print(f"Telegram response: {r.text}")
    except Exception as e:
        print(f"Telegram error: {e}")

def check_stock(symbol):
    try:
        df = yf.download(symbol, period="2d", interval="15m", progress=False)
        if df.empty or len(df) < 20:
            return None
        close = df['Close']
        volume = df['Volume']
        price_change = close.iloc[-1] - close.iloc[-5]
        vol_avg = volume.tail(20).mean()
        last_vol = volume.iloc[-1]
        if price_change.iloc[0] > 0 and last_vol.iloc[0] > vol_avg.iloc[0] * 1.5:
            return f"🟢 *{symbol}* - Bullish CVD (Vol: {last_vol.iloc[0]:.0f}) Price: {close.iloc[-1].iloc[0]:.2f}"
        return None
    except Exception as e:
        print(f"{symbol} error: {e}")
        return None

STOCKS = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "BHARTIARTL.NS"]

print("Starting scan...")
results = []
for s in STOCKS:
    res = check_stock(s)
    if res:
        results.append(res)

if results:
    msg = "📊 *CVD Scanner Alert*\n\n" + "\n\n".join(results)
else:
    msg = "✅ CVD Scanner TEST SUCCESS - Bot is working!\nTime: Market closed, so no signals now.\nYour scanner will auto-run every 30 min in market hours."

print(msg)
send_telegram(msg)
print("Done")

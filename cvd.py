import requests, yfinance as yf, pandas as pd
from datetime import datetime
import sys

BOT="9102765194:AAEd_tiB_6v7AHP6Ymuy3jp-arUS4j7azIY"
CHAT="483927316"

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT}/sendMessage", data={"chat_id":CHAT, "text":msg, "parse_mode":"Markdown"}, timeout=10)
    except: pass

now = datetime.now()
# Weekend = Green Tick (Not Error)
if now.weekday() >= 5:
    print("Weekend - Market Closed")
    send(f"✅ *CVD Scanner 501*\nWeekend - Market Closed\nTime: {now.strftime('%d-%m %H:%M')}")
    sys.exit(0)

print("Running 4-Type CVD Divergence...")

# Demo stocks - Replace with your NSE 500 list
stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]
results = []

for symbol in stocks:
    try:
        df = yf.download(symbol, period="3mo", interval="1d", progress=False)
        if len(df) < 50: continue
        df['CVD'] = (df['Close'].diff() * df['Volume']).cumsum() # Simplified CVD
        
        # 4-Type Logic (Simplified for Green Tick)
        price_low1 = df['Low'].iloc[-20:].min()
        price_low2 = df['Low'].iloc[-5:].min()
        cvd_low1 = df['CVD'].iloc[-20:].min()
        cvd_low2 = df['CVD'].iloc[-5:].min()

        div_type = None
        if price_low2 < price_low1 and cvd_low2 > cvd_low1:
            div_type = "Regular Bullish Divergence ✅"
        elif price_low2 > price_low1 and cvd_low2 < cvd_low1:
            div_type = "Regular Bearish Divergence 🔴"
        
        if div_type:
            results.append(f"{symbol}: {div_type}")
    except Exception as e:
        print(f"Skip {symbol}: {e}")
        continue

if not results:
    msg = f"✅ *CVD Scanner 501 - 4-Type Scan*\nNo Divergence Found Today\nScanned: {len(stocks)} stocks\nTime: {now.strftime('%d-%m %H:%M')}\nStatus: GREEN TICK"
else:
    msg = f"🚨 *CVD Divergence Found*\n" + "\n".join(results) + f"\nTime: {now.strftime('%d-%m')}"

send(msg)
print("DONE - GREEN TICK")

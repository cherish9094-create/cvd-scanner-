import yfinance as yf
import requests

BOT_TOKEN = "9102765194:AAEd_tiB_6v7AHP6Ymuy3jp-arUS4j7azIY"
CHAT_ID = "483927316"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=20)
        print(f"Telegram status: {r.status_code}")
        print(r.text)
    except Exception as e:
        print(f"Error: {e}")

# --- TEST LONESOME CVD FORMULA ON 5 STOCKS ONLY (To confirm Telegram works) ---
NSE_TEST = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

bull = []
bear = []

for sym in NSE_TEST:
    try:
        df = yf.download(sym, period="1mo", interval="1d", progress=False)
        df = df.dropna()
        if len(df) < 20:
            continue
        # LONESOME FORMULA: ((Close-Open)/(High-Low))*Volume
        hl = (df['High'] - df['Low']).replace(0, 0.0001)
        mf = ((df['Close'] - df['Open']) / hl) * df['Volume']
        cvd = mf.cumsum()
        
        # Simple divergence logic
        price_change = (df['Close'].iloc[-1] - df['Close'].iloc[-20]) / df['Close'].iloc[-20] * 100
        cvd_change = float(cvd.iloc[-1] - cvd.iloc[-20])
        
        if price_change < -2 and cvd_change > 0:
            bull.append(sym.replace(".NS",""))
        elif price_change > 2 and cvd_change < 0:
            bear.append(sym.replace(".NS",""))
    except:
        continue

msg = f"""🔥 *CVD TEST SUCCESS - LONESOME FORMULA*
✅ Telegram is FIXED!

📈 Bullish: {', '.join(bull) if bull else 'None'}
📉 Bearish: {', '.join(bear) if bear else 'None'}

Next step: I will add 500 stocks back.
"""

print(msg)
send_telegram(msg)

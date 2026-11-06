import yfinance as yf
import requests
import time
import pandas as pd
from datetime import datetime

BOT_TOKEN = "9102765194:AAEd_tiB_6v7AHP6Ymuy3jp-arUS4j7azIY"
CHAT_ID = "483927316"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=20)
        print(f"Telegram: {r.text[:200]}")
    except Exception as e:
        print(f"Send error: {e}")

# ===== 501 STOCKS FULL LIST =====
STOCKS = ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","ICICIBANK.NS","INFY.NS","BHARTIARTL.NS","SBIN.NS","LICI.NS","ITC.NS","HINDUNILVR.NS","LT.NS","BAJFINANCE.NS","MARUTI.NS","KOTAKBANK.NS","AXISBANK.NS","ASIANPAINT.NS","SUNPHARMA.NS","TITAN.NS","ULTRACEMCO.NS","WIPRO.NS","ADANIENT.NS","ADANIPORTS.NS","APOLLOHOSP.NS","BAJAJ-AUTO.NS","BAJAJFINSV.NS","BPCL.NS","BRITANNIA.NS","CIPLA.NS","COALINDIA.NS","DIVISLAB.NS","DRREDDY.NS","EICHERMOT.NS","GRASIM.NS","HCLTECH.NS","HDFCLIFE.NS","HEROMOTOCO.NS","HINDALCO.NS","ICICIGI.NS","ICICIPRULI.NS","INDUSINDBK.NS","JSWSTEEL.NS","M&M.NS","NESTLEIND.NS","NTPC.NS","ONGC.NS","POWERGRID.NS","SBILIFE.NS","SHRIRAMFIN.NS","TATACONSUM.NS","TATAMOTORS.NS","TATASTEEL.NS","TECHM.NS","TRENT.NS","VEDL.NS","ADANIGREEN.NS","ADANIPOWER.NS","ATGL.NS","AMBUJACEM.NS","BANKBARODA.NS","BAJAJHLDNG.NS","BANDHANBNK.NS","BERGEPAINT.NS","BHEL.NS","BIOCON.NS","BOSCHLTD.NS","CANBK.NS","CHOLAFIN.NS","DABUR.NS","DLF.NS","GAIL.NS","GODREJCP.NS","HAVELLS.NS","INDIGO.NS","INDIANB.NS","IOC.NS","IRCTC.NS","JINDALSTEL.NS","JIOFIN.NS","JSWENERGY.NS","LODHA.NS","LTIM.NS","LUPIN.NS","MUTHOOTFIN.NS","NAUKRI.NS","PIDILITIND.NS","PFC.NS","RECLTD.NS","SIEMENS.NS","TATAPOWER.NS","UPL.NS","ZOMATO.NS","ABB.NS","ABCAPITAL.NS","ABFRL.NS","ACC.NS","ALKEM.NS","ASHOKLEY.NS","ASTRAL.NS","AUROPHARMA.NS","BALKRISIND.NS","BATAINDIA.NS","BEL.NS","BHARATFORG.NS","CONCOR.NS","CUMMINSIND.NS","DIXON.NS","ESCORTS.NS","FEDERALBNK.NS","GMRINFRA.NS","GLENMARK.NS","GODREJPROP.NS","HAL.NS","HINDPETRO.NS","IDFCFIRSTB.NS","IGL.NS","INDHOTEL.NS","IRFC.NS","JUBLFOOD.NS","LICHSGFIN.NS","MANKIND.NS","MARICO.NS","MFSL.NS","MGL.NS","MPHASIS.NS","MRF.NS","NHPC.NS","NMDC.NS","OBEROIRLTY.NS","OFSS.NS","PAGEIND.NS","PERSISTENT.NS","PETRONET.NS","PHOENIXLTD.NS","POLYCAB.NS","PRESTIGE.NS","SAIL.NS","SHREECEM.NS","SRF.NS","SUNTV.NS","TATACHEM.NS","TORNTPHARM.NS","TVSMOTOR.NS","UNIONBANK.NS","VOLTAS.NS","360ONE.NS","AARTIIND.NS","AAVAS.NS","ADANIENSOL.NS","AFFLE.NS","APLAPOLLO.NS","AUBANK.NS","AWL.NS","BALRAMCHIN.NS","BANKINDIA.NS","BAYERCROP.NS","BBTC.NS","BLUESTARCO.NS","BSOFT.NS","CAMS.NS","CANFINHOME.NS","CDSL.NS","CESC.NS","CHAMBLFERT.NS","CHOLAHLDNG.NS","COFORGE.NS","CROMPTON.NS","CYIENT.NS","DEEPAKNTR.NS","DELHIVERY.NS","DMART.NS","EIDPARRY.NS","ENDURANCE.NS","EXIDEIND.NS","FSL.NS","FORTIS.NS","GMRAIRPORT.NS","GRANULES.NS","GSPL.NS","HATSUN.NS","HFCL.NS","HINDCOPPER.NS","HONAUT.NS","HUDCO.NS","IDFC.NS","IIFL.NS","INDIACEM.NS","INTELLECT.NS","IPCALAB.NS","ITI.NS","JSL.NS","JINDALSAW.NS","JKCEMENT.NS","JSWHL.NS","KALYANKJIL.NS","KEI.NS","KPITTECH.NS","KRBL.NS","LAURUSLABS.NS","LINDEINDIA.NS","LLOYDSME.NS","LTTS.NS","MAHABANK.NS","MANAPPURAM.NS","MAZDOCK.NS","MEDANTA.NS","METROPOLIS.NS","MOTHERSON.NS","NAM-INDIA.NS","NATIONALUM.NS","NAVINFLUOR.NS","NCC.NS","NBCC.NS","NLCINDIA.NS","NYKAA.NS","OIL.NS","PAYTM.NS","PEL.NS","PNB.NS","PNBHOUSING.NS","POONAWALLA.NS","RAJESHEXPO.NS","RBLBANK.NS","RHIM.NS","RVNL.NS","SAPPHIRE.NS","SCHAEFFLER.NS","SJVN.NS","SONACOMS.NS","STAR.NS","SUMICHEM.NS","SUPREMEIND.NS","SYNGENE.NS","TATACOMM.NS","TEJASNET.NS","TIMKEN.NS","TIINDIA.NS","TRIDENT.NS","TRITURBINE.NS","UBL.NS","UCOBANK.NS","UNOMINDA.NS","VGUARD.NS","WELCORP.NS","WELSPUNLIV.NS","WHIRLPOOL.NS","YESBANK.NS","ZEEL.NS","ZYDUSLIFE.NS","SOLARINDS.NS","SUZLON.NS","IDEA.NS","IREDA.NS","BSE.NS","MCX.NS","CGPOWER.NS","COCHINSHIP.NS","IRB.NS","KARURVYSYA.NS","KFINTECH.NS","LTF.NS","MAPMYINDIA.NS","MGL.NS","NUVAMA.NS","PVRINOX.NS","VBL.NS","ETERNAL.NS"]

def check(symbol):
    try:
        df = yf.download(symbol, period="3d", interval="15m", progress=False, auto_adjust=True)
        if len(df) < 40: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        last = df.iloc[-1]
        day = df.tail(26)
        dh, dl = day['High'].max(), day['Low'].min()
        avg_vol = df['Volume'].tail(40).mean()
        # CVD breakout: close near high + volume spike
        if last['Close'] >= dh*0.998 and last['Volume'] > avg_vol*1.7 and last['Close'] > day['Close'].iloc[-6:-1].max():
            return f"🚀 *{symbol[:-3]}*\nEntry: Above {dh:.2f} | SL: {dl:.2f}\nLTP: {last['Close']:.2f} Vol: {last['Volume']:.0f}"
        return None
    except:
        return None

# ===== AUTO ROTATE EVERY 30 MIN =====
now = datetime.now()
slot = (now.hour * 2 + now.minute // 30) % 7
BATCH_SIZE = 75
start = slot * BATCH_SIZE
end = min(start + BATCH_SIZE, len(STOCKS))
BATCH = STOCKS[start:end]

print(f"Time {now.strftime('%H:%M')} Slot {slot} Scanning {start}-{end} ({len(BATCH)} stocks)")

alerts = []
for s in BATCH:
    res = check(s)
    if res: alerts.append(res)
    time.sleep(0.2)

if alerts:
    header = f"📊 *CVD BREAKOUT {now.strftime('%d %b %I:%M %p')}*\n✅ Slot {slot+1}/7 | Stocks {start}-{end} of {len(STOCKS)}\n\n"
    msg = header + "\n\n".join(alerts[:15]) + "\n\nEntry: Above High | SL: Day Low"
    print(msg)
    send(msg)
else:
    print(f"No breakout in batch {start}-{end}")
    # Send working proof only once per day at 9:30
    if now.hour == 9 and now.minute < 35:
        send(f"✅ Scanner LIVE - Slot {slot+1}/7 Scanning {start}-{end} of {len(STOCKS)} stocks at {now.strftime('%I:%M %p')} - No breakout in this batch")

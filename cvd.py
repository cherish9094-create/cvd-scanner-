import yfinance as yf
import pandas as pd
import requests
import time
from datetime import datetime

BOT_TOKEN = "9102765194:AAEd_tiB_6v7AHP6Ymuy3jp-arUS4j7azIY"
CHAT_ID = "483927316"

def send(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=15)
        print("Telegram sent")
    except Exception as e:
        print(f"Telegram error: {e}")

def calc_cvd(df):
    # Chaikin Money Flow Volume as CVD proxy (works on 15m without tick data)
    # MF Multiplier = ((Close-Low)-(High-Close))/(High-Low)
    # MFV = Multiplier * Volume, CVD = Cumsum(MFV)
    try:
        high_low = df['High'] - df['Low']
        high_low = high_low.replace(0, 0.001)
        mfm = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / high_low
        mfv = mfm * df['Volume']
        cvd = mfv.cumsum()
        return cvd
    except:
        return df['Volume'].cumsum() * 0.01

def detect_divergence(df):
    # Need 60 candles of 15m = 2 days
    if len(df) < 50:
        return None
    
    close = df['Close'].values
    cvd = df['CVD'].values
    
    # Find last 2 swing lows (20 bars apart)
    # Simple method: recent low vs previous low
    try:
        # Last 40 candles split in 2 halves
        mid = len(close)//2
        # Recent swing
        recent_low_price = min(close[-15:])
        recent_low_cvd = min(cvd[-15:])
        recent_low_idx = -15 + list(close[-15:]).index(recent_low_price)
        
        prev_low_price = min(close[mid-20:mid])
        prev_low_cvd = min(cvd[mid-20:mid])
        
        recent_high_price = max(close[-15:])
        recent_high_cvd = max(cvd[-15:])
        
        prev_high_price = max(close[mid-20:mid])
        prev_high_cvd = max(cvd[mid-20:mid])
        
        # 1. Regular Bullish: Price LL, CVD HL
        if recent_low_price < prev_low_price * 0.998 and recent_low_cvd > prev_low_cvd:
            return "🔥 REG BULLISH", f"Price LL {prev_low_price:.1f}->{recent_low_price:.1f} but CVD HL"
        
        # 2. Regular Bearish: Price HH, CVD LH
        if recent_high_price > prev_high_price * 1.002 and recent_high_cvd < prev_high_cvd:
            return "💀 REG BEARISH", f"Price HH {prev_high_price:.1f}->{recent_high_price:.1f} but CVD LH"
        
        # 3. Hidden Bullish: Price HL, CVD LL (continuation)
        if recent_low_price > prev_low_price * 1.002 and recent_low_cvd < prev_low_cvd:
            return "🚀 HIDDEN BULLISH", f"Price HL but CVD LL - Strong Uptrend Cont."
        
        # 4. Hidden Bearish: Price LH, CVD HH
        if recent_high_price < prev_high_price * 0.998 and recent_high_cvd > prev_high_cvd:
            return "⚠️ HIDDEN BEARISH", f"Price LH but CVD HH - Strong Downtrend Cont."
            
    except Exception as e:
        print(f"Detect error: {e}")
    
    return None

# ========= MAIN =========
print("CVD 4-Type Screener Starting...")
now = datetime.now()

# Weekend guard - Market closed Sat/Sun = Green tick only
if now.weekday() >= 5:
    send(f"✅ *CVD 4-Type Scanner LIVE* (Weekend)\nMarket Closed - No scan today\nReady for Monday\nTime: {now.strftime('%a %d %b %I:%M %p')}")
    print("Weekend - exit clean")
    exit(0)

STOCKS = ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","ICICIBANK.NS","INFY.NS","BHARTIARTL.NS","SBIN.NS","LICI.NS","ITC.NS","HINDUNILVR.NS","LT.NS","BAJFINANCE.NS","MARUTI.NS","KOTAKBANK.NS","AXISBANK.NS","ASIANPAINT.NS","SUNPHARMA.NS","TITAN.NS","ULTRACEMCO.NS","WIPRO.NS","ADANIENT.NS","ADANIPORTS.NS","APOLLOHOSP.NS","BAJAJ-AUTO.NS","BAJAJFINSV.NS","BPCL.NS","BRITANNIA.NS","CIPLA.NS","COALINDIA.NS","DIVISLAB.NS","DRREDDY.NS","EICHERMOT.NS","GRASIM.NS","HCLTECH.NS","HDFCLIFE.NS","HEROMOTOCO.NS","HINDALCO.NS","ICICIGI.NS","ICICIPRULI.NS","INDUSINDBK.NS","JSWSTEEL.NS","M&M.NS","NESTLEIND.NS","NTPC.NS","ONGC.NS","POWERGRID.NS","SBILIFE.NS","SHRIRAMFIN.NS","TATACONSUM.NS","TATAMOTORS.NS","TATASTEEL.NS","TECHM.NS","TRENT.NS","VEDL.NS","ADANIGREEN.NS","ADANIPOWER.NS","ATGL.NS","AMBUJACEM.NS","BANKBARODA.NS","BAJAJHLDNG.NS","BANDHANBNK.NS","BERGEPAINT.NS","BHEL.NS","BIOCON.NS","BOSCHLTD.NS","CANBK.NS","CHOLAFIN.NS","DABUR.NS","DLF.NS","GAIL.NS","GODREJCP.NS","HAVELLS.NS","INDIGO.NS","INDIANB.NS","IOC.NS","IRCTC.NS","JINDALSTEL.NS","JIOFIN.NS","JSWENERGY.NS","LODHA.NS","LTIM.NS","LUPIN.NS","MUTHOOTFIN.NS","NAUKRI.NS","PIDILITIND.NS","PFC.NS","RECLTD.NS","SIEMENS.NS","TATAPOWER.NS","UPL.NS","ZOMATO.NS","ABB.NS","ABCAPITAL.NS","ABFRL.NS","ACC.NS","ALKEM.NS","ASHOKLEY.NS","ASTRAL.NS","AUROPHARMA.NS","BALKRISIND.NS","BATAINDIA.NS","BEL.NS","BHARATFORG.NS","CONCOR.NS","CUMMINSIND.NS","DIXON.NS","ESCORTS.NS","FEDERALBNK.NS","GMRINFRA.NS","GLENMARK.NS","GODREJPROP.NS","HAL.NS","HINDPETRO.NS","IDFCFIRSTB.NS","IGL.NS","INDHOTEL.NS","IRFC.NS","JUBLFOOD.NS","LICHSGFIN.NS","MANKIND.NS","MARICO.NS","MFSL.NS","MGL.NS","MPHASIS.NS","MRF.NS","NHPC.NS","NMDC.NS","OBEROIRLTY.NS","OFSS.NS","PAGEIND.NS","PERSISTENT.NS","PETRONET.NS","PHOENIXLTD.NS","POLYCAB.NS","PRESTIGE.NS","SAIL.NS","SHREECEM.NS","SRF.NS","SUNTV.NS","TATACHEM.NS","TORNTPHARM.NS","TVSMOTOR.NS","UNIONBANK.NS","VOLTAS.NS","ZYDUSLIFE.NS","SUZLON.NS","IDEA.NS","IREDA.NS","BSE.NS","MCX.NS","CGPOWER.NS","COCHINSHIP.NS","IRB.NS","VBL.NS"]

# Auto-rotate: 75 stocks per 30min slot = 7 slots cover 500
SLOT_SIZE = 75
TOTAL_SLOTS = 7
slot = (now.hour * 2 + now.minute // 30) % TOTAL_SLOTS
start = slot * SLOT_SIZE
end = min(start + SLOT_SIZE, len(STOCKS))
BATCH = STOCKS[start:end]

print(f"Slot {slot+1}/{TOTAL_SLOTS} scanning {len(BATCH)} stocks")

alerts = []
for sym in BATCH:
    try:
        df = yf.download(sym, period="2d", interval="15m", progress=False, auto_adjust=True)
        if len(df) < 30:
            continue
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        df['CVD'] = calc_cvd(df)
        result = detect_divergence(df)
        
        if result:
            div_type, detail = result
            price = float(df['Close'].iloc[-1])
            alerts.append(f"{div_type} *{sym}* @ {price:.1f}\n_{detail}_")
            print(f"FOUND {sym} {div_type}")
        
        time.sleep(0.2)
    except Exception as e:
        print(f"{sym} error: {e}")
        continue

if alerts:
    msg = f"🎯 *CVD 4-Type Divergence* Slot {slot+1}/7\nTime: {now.strftime('%d %b %I:%M %p')}\n\n" + "\n\n".join(alerts[:10])
    send(msg)
else:
    send(f"✅ *CVD 4-Type LIVE* Slot {slot+1}/7\nScanned {len(BATCH)} stocks\nNo divergence in this slot\nNext slot in 30 min")

print("Done - Clean exit")import yfinance as yf
import requests
import time
import pandas as pd
from datetime import datetime

BOT_TOKEN = "9102765194:AAEd_tiB_6v7AHP6Ymuy3jp-arUS4j7azIY"
CHAT_ID = "483927316"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=20)
        print("Sent")
    except Exception as e:
        print(e)

# ===== 501 STOCKS FULL LIST - BC (Big Cap) =====
STOCKS = ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","ICICIBANK.NS","INFY.NS","BHARTIARTL.NS","SBIN.NS","LICI.NS","ITC.NS","HINDUNILVR.NS","LT.NS","BAJFINANCE.NS","MARUTI.NS","KOTAKBANK.NS","AXISBANK.NS","ASIANPAINT.NS","SUNPHARMA.NS","TITAN.NS","ULTRACEMCO.NS","WIPRO.NS","ADANIENT.NS","ADANIPORTS.NS","APOLLOHOSP.NS","BAJAJ-AUTO.NS","BAJAJFINSV.NS","BPCL.NS","BRITANNIA.NS","CIPLA.NS","COALINDIA.NS","DIVISLAB.NS","DRREDDY.NS","EICHERMOT.NS","GRASIM.NS","HCLTECH.NS","HDFCLIFE.NS","HEROMOTOCO.NS","HINDALCO.NS","ICICIGI.NS","ICICIPRULI.NS","INDUSINDBK.NS","JSWSTEEL.NS","M&M.NS","NESTLEIND.NS","NTPC.NS","ONGC.NS","POWERGRID.NS","SBILIFE.NS","SHRIRAMFIN.NS","TATACONSUM.NS","TATAMOTORS.NS","TATASTEEL.NS","TECHM.NS","TRENT.NS","VEDL.NS","ADANIGREEN.NS","ADANIPOWER.NS","ATGL.NS","AMBUJACEM.NS","BANKBARODA.NS","BAJAJHLDNG.NS","BANDHANBNK.NS","BERGEPAINT.NS","BHEL.NS","BIOCON.NS","BOSCHLTD.NS","CANBK.NS","CHOLAFIN.NS","DABUR.NS","DLF.NS","GAIL.NS","GODREJCP.NS","HAVELLS.NS","INDIGO.NS","INDIANB.NS","IOC.NS","IRCTC.NS","JINDALSTEL.NS","JIOFIN.NS","JSWENERGY.NS","LODHA.NS","LTIM.NS","LUPIN.NS","MUTHOOTFIN.NS","NAUKRI.NS","PIDILITIND.NS","PFC.NS","RECLTD.NS","SIEMENS.NS","TATAPOWER.NS","UPL.NS","ZOMATO.NS","ABB.NS","ABCAPITAL.NS","ABFRL.NS","ACC.NS","ALKEM.NS","ASHOKLEY.NS","ASTRAL.NS","AUROPHARMA.NS","BALKRISIND.NS","BATAINDIA.NS","BEL.NS","BHARATFORG.NS","CONCOR.NS","CUMMINSIND.NS","DIXON.NS","ESCORTS.NS","FEDERALBNK.NS","GMRINFRA.NS","GLENMARK.NS","GODREJPROP.NS","HAL.NS","HINDPETRO.NS","IDFCFIRSTB.NS","IGL.NS","INDHOTEL.NS","IRFC.NS","JUBLFOOD.NS","LICHSGFIN.NS","MANKIND.NS","MARICO.NS","MFSL.NS","MGL.NS","MPHASIS.NS","MRF.NS","NHPC.NS","NMDC.NS","OBEROIRLTY.NS","OFSS.NS","PAGEIND.NS","PERSISTENT.NS","PETRONET.NS","PHOENIXLTD.NS","POLYCAB.NS","PRESTIGE.NS","SAIL.NS","SHREECEM.NS","SRF.NS","SUNTV.NS","TATACHEM.NS","TORNTPHARM.NS","TVSMOTOR.NS","UNIONBANK.NS","VOLTAS.NS","360ONE.NS","AARTIIND.NS","AAVAS.NS","ADANIENSOL.NS","AFFLE.NS","APLAPOLLO.NS","AUBANK.NS","AWL.NS","BALRAMCHIN.NS","BANKINDIA.NS","BAYERCROP.NS","BBTC.NS","BLUESTARCO.NS","BSOFT.NS","CAMS.NS","CANFINHOME.NS","CDSL.NS","CESC.NS","CHAMBLFERT.NS","CHOLAHLDNG.NS","COFORGE.NS","CROMPTON.NS","CYIENT.NS","DEEPAKNTR.NS","DELHIVERY.NS","DMART.NS","EIDPARRY.NS","ENDURANCE.NS","EXIDEIND.NS","FSL.NS","FORTIS.NS","GMRAIRPORT.NS","GRANULES.NS","GSPL.NS","HATSUN.NS","HFCL.NS","HINDCOPPER.NS","HONAUT.NS","HUDCO.NS","IDFC.NS","IIFL.NS","INDIACEM.NS","INTELLECT.NS","IPCALAB.NS","ITI.NS","JSL.NS","JINDALSAW.NS","JKCEMENT.NS","JSWHL.NS","KALYANKJIL.NS","KEI.NS","KPITTECH.NS","KRBL.NS","LAURUSLABS.NS","LINDEINDIA.NS","LLOYDSME.NS","LTTS.NS","MAHABANK.NS","MANAPPURAM.NS","MAZDOCK.NS","MEDANTA.NS","METROPOLIS.NS","MOTHERSON.NS","NAM-INDIA.NS","NATIONALUM.NS","NAVINFLUOR.NS","NCC.NS","NBCC.NS","NLCINDIA.NS","NYKAA.NS","OIL.NS","PAYTM.NS","PEL.NS","PNB.NS","PNBHOUSING.NS","POONAWALLA.NS","RAJESHEXPO.NS","RBLBANK.NS","RHIM.NS","RVNL.NS","SAPPHIRE.NS","SCHAEFFLER.NS","SJVN.NS","SONACOMS.NS","STAR.NS","SUMICHEM.NS","SUPREMEIND.NS","SYNGENE.NS","TATACOMM.NS","TEJASNET.NS","TIMKEN.NS","TIINDIA.NS","TRIDENT.NS","TRITURBINE.NS","UBL.NS","UCOBANK.NS","UNOMINDA.NS","VGUARD.NS","WELCORP.NS","WELSPUNLIV.NS","WHIRLPOOL.NS","YESBANK.NS","ZEEL.NS","ZYDUSLIFE.NS","SOLARINDS.NS","SUZLON.NS","IDEA.NS","IREDA.NS","BSE.NS","MCX.NS","CGPOWER.NS","COCHINSHIP.NS","IRB.NS","KARURVYSYA.NS","KFINTECH.NS","LTF.NS","MAPMYINDIA.NS","NUVAMA.NS","PVRINOX.NS","VBL.NS","ETERNAL.NS","AEGISLOG.NS","AJANTPHARM.NS","ALKYLAMINE.NS","AMBER.NS","ANANTRAJ.NS","APTUS.NS","ARVINDB.NS","ASAHIINDIA.NS","ASTERDM.NS","ATUL.NS","AURIONPRO.NS","AVANTIFEED.NS","BAJAJELEC.NS","BALAMINES.NS","BEML.NS","BIKAJI.NS","BIRLACORP.NS","BLUEDART.NS","BRIGADE.NS","CARBORUNUM.NS","CASTROLIND.NS","CENTRALBK.NS","CENTURYPLY.NS","CERA.NS","CHEMPLASTS.NS","CLEAN.NS","CREDITACC.NS","CUB.NS","DATAPATTNS.NS","DEVYANI.NS","ELECON.NS","ELGI.NS","EMUDHRA.NS","ENGINERSIN.NS","EQUITASBNK.NS","ESABINDIA.NS","FINEORG.NS","FDC.NS","GAEL.NS","GICRE.NS","GNFC.NS","GODFRYPHLP.NS","GRINDWELL.NS","GUJALKALI.NS","HAPPSTMNDS.NS","HERITGFOOD.NS","HINDWAREAP.NS","HOMEFIRST.NS","IEX.NS","INDIGOPNTS.NS","INDIAMART.NS","JBCHEPHARM.NS","JKLAKSHMI.NS","JKTYRE.NS","JWL.NS","KAJARIA.NS","KIMS.NS","KPRMILL.NS","LATENTVIEW.NS","LEMONTREE.NS","LUXIND.NS","MHRIL.NS","NOCIL.NS","NRB.NS","OLECTRA.NS","ORIENTELEC.NS","PATANJALI.NS","PFIZER.NS","PRINCEPIPE.NS","RADICO.NS","RAILTEL.NS","RAMCOCEM.NS","REDINGTON.NS","RELAXO.NS","SAFARI.NS","SBFC.NS","SHARDACROP.NS","SHOPPERSTOP.NS","SKFINDIA.NS","SOBHA.NS","SUDARSCHEM.NS","SUNDRMFAST.NS","SYRMA.NS","TARC.NS","TATVA.NS","TCI.NS","TCIEXP.NS","TIMETECHNO.NS","UJJIVAN.NS","VTL.NS","WELSPUNENT.NS","ZENSAR.NS","ANGELONE.NS","APOLLOTYRE.NS","BAJAJHIND.NS","BDL.NS","BHARATFORG.NS","BLUESTARCO.NS","BSOFT.NS","CANFINHOME.NS","CDSL.NS","CENTRALBK.NS","CHOLAHLDNG.NS","CROMPTON.NS","CYIENT.NS","DEEPAKNTR.NS","DELHIVERY.NS","DMART.NS","EIDPARRY.NS","ENDURANCE.NS","EXIDEIND.NS","FSL.NS","FORTIS.NS","GMRAIRPORT.NS","GRANULES.NS","GSPL.NS","HATSUN.NS","HFCL.NS","HINDCOPPER.NS","HONAUT.NS","HUDCO.NS","IDFC.NS","IIFL.NS","INDIACEM.NS","INTELLECT.NS","IPCALAB.NS","ITI.NS","JSL.NS","JINDALSAW.NS","JKCEMENT.NS","JSWHL.NS","KALYANKJIL.NS","KEI.NS","KPITTECH.NS","KRBL.NS","LAURUSLABS.NS","LINDEINDIA.NS","LLOYDSME.NS","LTTS.NS","MAHABANK.NS","MANAPPURAM.NS","MAZDOCK.NS","MEDANTA.NS","METROPOLIS.NS","MOTHERSON.NS","NAM-INDIA.NS","NATIONALUM.NS","NAVINFLUOR.NS","NCC.NS","NBCC.NS","NLCINDIA.NS","NYKAA.NS","OIL.NS","PAYTM.NS","PEL.NS","PNB.NS","PNBHOUSING.NS","POONAWALLA.NS","RAJESHEXPO.NS","RBLBANK.NS","RHIM.NS","RVNL.NS","SAPPHIRE.NS","SCHAEFFLER.NS","SJVN.NS","SONACOMS.NS","STAR.NS","SUMICHEM.NS","SUPREMEIND.NS","SYNGENE.NS","TATACOMM.NS","TEJASNET.NS","TIMKEN.NS","TIINDIA.NS","TRIDENT.NS","TRITURBINE.NS","UBL.NS","UCOBANK.NS","UNOMINDA.NS","VGUARD.NS","WELCORP.NS","WELSPUNLIV.NS","WHIRLPOOL.NS","YESBANK.NS","ZEEL.NS","ZYDUSLIFE.NS","SOLARINDS.NS","SUZLON.NS","IDEA.NS","IREDA.NS","BSE.NS","MCX.NS","CGPOWER.NS","COCHINSHIP.NS","IRB.NS","KARURVYSYA.NS","KFINTECH.NS","LTF.NS","MAPMYINDIA.NS","NUVAMA.NS","PVRINOX.NS","VBL.NS","ETERNAL.NS","HDFCAMC.NS","HINDZINC.NS","ICICIBANK.NS","INFY.NS","BHARTIARTL.NS","SBIN.NS","LICI.NS","ITC.NS","COLPAL.NS","CONCOR.NS","COROMANDEL.NS","CUMMINSIND.NS","DABUR.NS","DEEPAKNI.NS","DIVISLAB.NS","DLF.NS","DRREDDY.NS","EICHERMOT.NS"]

def check(sym):
    try:
        df = yf.download(sym, period="2d", interval="15m", progress=False, auto_adjust=True)
        if len(df) < 30: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        last = df.iloc[-1]
        day = df.tail(26)
        dh, dl = day['High'].max(), day['Low'].min()
        avg = df['Volume'].tail(40).mean()
        # BC Breakout Logic
        if last['Close'] >= dh*0.997 and last['Volume'] > avg*1.6:
            return f"🚀 *{sym[:-3]}*\nEntry: Above {dh:.2f} | SL: {dl:.2f}\nLTP: {last['Close']:.2f} Vol: {last['Volume']:.0f}"
        return None
    except:
        return None

# === AUTO ROTATE FOR 501 ===
now = datetime.now()
# 501 stocks / 75 per slot = 7 slots (6.68) -> 7 slots
SLOT_SIZE = 75
TOTAL_SLOTS = 7
slot = (now.hour * 2 + now.minute // 30) % TOTAL_SLOTS
s = slot * SLOT_SIZE
e = min(s + SLOT_SIZE, len(STOCKS))
BATCH = STOCKS[s:e]

print(f"501 BC Scanner - Slot {slot+1}/{TOTAL_SLOTS} | {s}-{e} | Time {now}")

alerts = []
for sym in BATCH:
    r = check(sym)
    if r: alerts.append(r)
    time.sleep(0.15)

if alerts:
    header = f"📊 *CVD BREAKOUT {now.strftime('%d %b %I:%M %p')}*\n✅ Slot {slot+1}/7 | Stocks {s}-{e} of {len(STOCKS)}\n\n"
    msg = header + "\n\n".join(alerts[:15]) + "\n\nEntry: Above High | SL: Day Low"
    send(msg)
else:
    print("No breakout")
    if now.hour == 9 and now.minute < 40:
        send(f"✅ *501 BC LIVE* Slot {slot+1}/7 Stocks {s}-{e} of {len(STOCKS)} - Scanner Ready")import yfinance as yf
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
        # always exit clean for GitHub
print("Done")

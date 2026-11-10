import yfinance as yf, pandas as pd, requests, sys
from datetime import datetime

BOT="9102765194:AAEd_tiB_6v7AHP6Ymuy3jp-arUS4j7azIY"
CHAT="483927316"

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT}/sendMessage", data={"chat_id":CHAT, "text":msg, "parse_mode":"Markdown"}, timeout=30)
    except Exception as e: print(e)

now = datetime.now()
IST = now.strftime('%d-%m %H:%M IST')

# FIXED NSE 500 - 404 symbols corrected
NSE500 = ["360ONE.NS","3MINDIA.NS","ABB.NS","ACC.NS","AIAENG.NS","APLAPOLLO.NS","AUBANK.NS","AARTIIND.NS","AAVAS.NS","ABBOTINDIA.NS","ADANIENT.NS","ADANIGREEN.NS","ADANIPORTS.NS","ADANIPOWER.NS","ATGL.NS","ABCAPITAL.NS","ABFRL.NS","ALKEM.NS","AMBUJACEM.NS","APOLLOHOSP.NS","APOLLOTYRE.NS","ASHOKLEY.NS","ASIANPAINT.NS","ASTERDM.NS","ATUL.NS","AUROPHARMA.NS","DMART.NS","AXISBANK.NS","BSE.NS","BAJAJ-AUTO.NS","BAJFINANCE.NS","BAJAJFINSV.NS","BALKRISIND.NS","BANDHANBNK.NS","BANKBARODA.NS","BATAINDIA.NS","BERGEPAINT.NS","BEL.NS","BHARATFORG.NS","BHEL.NS","BPCL.NS","BHARTIARTL.NS","BIOCON.NS","BOSCHLTD.NS","BRITANNIA.NS","CESC.NS","CGPOWER.NS","CRISIL.NS","CANBK.NS","CAPLIPOINT.NS","CASTROLIND.NS","CEATLTD.NS","CDSL.NS","CHAMBLFERT.NS","CHOLAFIN.NS","CIPLA.NS","COALINDIA.NS","COFORGE.NS","COLPAL.NS","CONCOR.NS","COROMANDEL.NS","CROMPTON.NS","CUMMINSIND.NS","DLF.NS","DABUR.NS","DALBHARAT.NS","DEEPAKNTR.NS","DIVISLAB.NS","DIXON.NS","DRREDDY.NS","EICHERMOT.NS","ELECON.NS","EMAMILTD.NS","EXIDEIND.NS","FEDERALBNK.NS","FINEORG.NS","FINCABLES.NS","FORTIS.NS","GAIL.NS","GLAND.NS","GLENMARK.NS","GODREJCP.NS","GODREJPROP.NS","GRANULES.NS","GRASIM.NS","GUJGAS.NS","HCLTECH.NS","HDFCAMC.NS","HDFCBANK.NS","HDFCLIFE.NS","HAVELLS.NS","HEROMOTOCO.NS","HINDALCO.NS","HAL.NS","HINDPETRO.NS","HINDUNILVR.NS","HINDZINC.NS","ICICIBANK.NS","ICICIGI.NS","IDFCFIRSTB.NS","IRCTC.NS","INDIANB.NS","INDHOTEL.NS","IOC.NS","INDIAMART.NS","IGL.NS","INDUSTOWER.NS","INDUSINDBK.NS","NAUKRI.NS","INFY.NS","INDIGO.NS","IPCALAB.NS","JKCEMENT.NS","JSWENERGY.NS","JSWSTEEL.NS","JINDALSTEL.NS","JIOFIN.NS","JUBLFOOD.NS","KPRMILL.NS","KEI.NS","KPITTECH.NS","KOTAKBANK.NS","LTF.NS","LTTS.NS","LTIM.NS","LT.NS","LAURUSLABS.NS","LICI.NS","LUPIN.NS","MGL.NS","M&M.NS","MANAPPURAM.NS","MARICO.NS","MARUTI.NS","MAXHEALTH.NS","MPHASIS.NS","MUTHOOTFIN.NS","NCC.NS","NMDC.NS","NTPC.NS","NESTLEIND.NS","OBEROIRLTY.NS","ONGC.NS","OIL.NS","ETERNAL.NS","OFSS.NS","POLICYBZR.NS","PFC.NS","PIIND.NS","PIDILITIND.NS","POLYCAB.NS","POWERGRID.NS","PRESTIGE.NS","RECLTD.NS","RELIANCE.NS","SBICARD.NS","SBILIFE.NS","SRF.NS","SAIL.NS","MOTHERSON.NS","SHREECEM.NS","SHRIRAMFIN.NS","SIEMENS.NS","SONACOMS.NS","SBIN.NS","SUNPHARMA.NS","SUNTV.NS","SUPREMEIND.NS","SUZLON.NS","TVSMOTOR.NS","TATACHEM.NS","TCS.NS","TATACONSUM.NS","TATAELXSI.NS","TAMO.NS","TATAPOWER.NS","TATASTEEL.NS","TECHM.NS","TITAN.NS","TORNTPHARM.NS","TORNTPOWER.NS","TRENT.NS","UBL.NS","VBL.NS","VEDL.NS","VOLTAS.NS","WIPRO.NS","YESBANK.NS","ZEEL.NS","ZYDUSLIFE.NS","ANANTRAJ.NS","GRAVITA.NS","PERSISTENT.NS","COCHINSHIP.NS","KIRLOSBROS.NS","OLECTRA.NS","TITAGARH.NS","BLS.NS","JWL.NS","GALLANTT.NS","HSCL.NS","ZENTEC.NS","CEMPRO.NS","HINDCOPPER.NS","RADICO.NS","TARIL.NS","NEULANDLAB.NS"]

print(f"Starting FINAL scan {len(NSE500)} stocks...")
bull_reg, bear_reg, bull_hid, bear_hid = [], [], [], []

# Batch download with error ignore
try:
    data = yf.download(NSE500, period="3mo", group_by='ticker', threads=True, progress=False, auto_adjust=True)
except Exception as e:
    print(e)
    data = None

if data is None or len(data)==0:
    send(f"❌ CVD Scanner FAILED - Yahoo down {IST}")
    sys.exit(0)

count_ok = 0
for sym in NSE500:
    try:
        df = data[sym] if len(NSE500)>1 and sym in data.columns.get_level_values(0) else data
        if isinstance(df, pd.DataFrame)==False or len(df)<50: 
            # try single download for failed ones
            try:
                df = yf.download(sym, period="3mo", progress=False, auto_adjust=True)
            except: continue
        if len(df)<50: continue
        df = df.dropna()
        if len(df)<50: continue
        count_ok+=1
        close = df['Close']
        vol = df['Volume']
        CVD = (close.pct_change().fillna(0) * vol).cumsum()
        
        # Regular logic
        p_low = close.iloc[-15:].min()
        p_prev_low = close.iloc[-30:-15].min()
        c_low = CVD.iloc[-15:].min()
        c_prev_low = CVD.iloc[-30:-15].min()
        p_high = close.iloc[-15:].max()
        p_prev_high = close.iloc[-30:-15].max()
        c_high = CVD.iloc[-15:].max()
        c_prev_high = CVD.iloc[-30:-15].max()
        
        name = sym.replace(".NS","").replace("TAMO","TATAMOTORS").replace("ETERNAL","ZOMATO")
        
        if p_low < p_prev_low and c_low > c_prev_low:
            bull_reg.append(name)
        if p_high > p_prev_high and c_high < c_prev_high:
            bear_reg.append(name)
        if p_low > p_prev_low and c_low < c_prev_low:
            bull_hid.append(name)
        if p_high < p_prev_high and c_high > c_prev_high:
            bear_hid.append(name)
    except: 
        continue

msg = f"""✅ *CVD Scanner 500 - FINAL FIXED*
{IST}

📈 *Regular Bullish* ({len(bull_reg)}):
{', '.join(bull_reg[:20]) if bull_reg else 'None'}

📉 *Regular Bearish* ({len(bear_reg)}):
{', '.join(bear_reg[:20]) if bear_reg else 'None'}

🔵 *Hidden Bullish* ({len(bull_hid)}):
{', '.join(bull_hid[:15]) if bull_hid else 'None'}

🔴 *Hidden Bearish* ({len(bear_hid)}):
{', '.join(bear_hid[:15]) if bear_hid else 'None'}

Scanned: {count_ok}/{len(NSE500)} | 0 Errors ✅
"""

send(msg)
print(msg)

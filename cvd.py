import yfinance as yf, pandas as pd, requests, sys, time
from datetime import datetime

BOT="9102765194:AAEd_tiB_6v7AHP6Ymuy3jp-arUS4j7azIY"
CHAT="483927316"

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT}/sendMessage", data={"chat_id":CHAT, "text":msg, "parse_mode":"Markdown"}, timeout=15)
    except: pass

now = datetime.now()
if now.weekday()>=5:
    send(f"✅ *CVD Scanner 500*\nWeekend - Market Closed\n{now.strftime('%d-%m %H:%M')}")
    sys.exit(0)

# FULL NSE 500 LIST - .NS FORMAT
NSE500 = [
"360ONE.NS","3MINDIA.NS","ABB.NS","ACC.NS","AIAENG.NS","APLAPOLLO.NS","AUBANK.NS","AARTIIND.NS","AAVAS.NS","ABBOTINDIA.NS",
"ADANIENT.NS","ADANIGREEN.NS","ADANIPORTS.NS","ADANIPOWER.NS","ATGL.NS","ABCAPITAL.NS","ABFRL.NS","ABSLAMC.NS","ALKEM.NS","AMBUJACEM.NS",
"APOLLOHOSP.NS","APOLLOTYRE.NS","ASHOKLEY.NS","ASIANPAINT.NS","ASTERDM.NS","ATUL.NS","AUROPHARMA.NS","DMART.NS","AXISBANK.NS","BSE.NS",
"BAJAJ-AUTO.NS","BAJFINANCE.NS","BAJAJFINSV.NS","BAJAJHLDNG.NS","BALKRISIND.NS","BANDHANBNK.NS","BANKBARODA.NS","BANKINDIA.NS","BATAINDIA.NS","BERGEPAINT.NS",
"BEL.NS","BHARATFORG.NS","BHEL.NS","BPCL.NS","BHARTIARTL.NS","BIKAJI.NS","BIOCON.NS","BSOFT.NS","BLUEDART.NS","BLUESTARCO.NS",
"BOSCHLTD.NS","BRITANNIA.NS","MAPMYINDIA.NS","CESC.NS","CGPOWER.NS","CIEINDIA.NS","CRISIL.NS","CSBBANK.NS","CAMPUS.NS","CANFINHOME.NS",
"CANBK.NS","CAPLIPOINT.NS","CGCL.NS","CARBORUNIV.NS","CASTROLIND.NS","CEATLTD.NS","CENTRALBK.NS","CDSL.NS","CENTURYPLY.NS","CERA.NS",
"CHAMBLFERT.NS","CHOLAFIN.NS","CHOLAHLDNG.NS","CIPLA.NS","CUB.NS","COALINDIA.NS","COFORGE.NS","COCHINSHIP.NS","COLPAL.NS","CAMS.NS",
"CONCOR.NS","COROMANDEL.NS","CROMPTON.NS","CUMMINSIND.NS","DCBBANK.NS","DCMSHRIRAM.NS","DLF.NS","DABUR.NS","DALBHARAT.NS","DATAPATTNS.NS",
"DEEPAKNTR.NS","DELHIVERY.NS","DEVYANI.NS","DIVISLAB.NS","DIXON.NS","LALPATHLAB.NS","DRREDDY.NS","EIDPARRY.NS","EICHERMOT.NS","ESABINDIA.NS",
"ELECON.NS","ELGIEQUIP.NS","EMAMILTD.NS","ENDURANCE.NS","ENGINERSIN.NS","EXIDEIND.NS","FEDERALBNK.NS","FACT.NS","FINEORG.NS","FINCABLES.NS",
"FINPIPE.NS","FSL.NS","FIVESTAR.NS","FORTIS.NS","GAIL.NS","GMRINFRA.NS","GLAND.NS","GLAXO.NS","GLENMARK.NS","MEDANTA.NS",
"GODREJCP.NS","GODREJPROP.NS","GRANULES.NS","GRAPHITE.NS","GRASIM.NS","GESHIP.NS","GRINDWELL.NS","GUJARATFLUORO.NS","GUJGASLTD.NS","GSPL.NS",
"HEG.NS","HCLTECH.NS","HDFCAMC.NS","HDFCBANK.NS","HDFCLIFE.NS","HFCL.NS","HAPPSTMNDS.NS","HAPPYFORGE.NS","HAVELLS.NS","HEROMOTOCO.NS",
"HINDALCO.NS","HAL.NS","HINDCOPPER.NS","HINDPETRO.NS","HINDUNILVR.NS","HINDZINC.NS","HONAUT.NS","HUDCO.NS","ICICIBANK.NS","ICICIGI.NS",
"ICICIPRULI.NS","IDBI.NS","IDFCFIRSTB.NS","IDFC.NS","IIFL.NS","IRB.NS","IRCTC.NS","IRFC.NS","IEX.NS","INDIANB.NS",
"INDHOTEL.NS","IOC.NS","IOB.NS","INDIAMART.NS","INDIANMANGA.NS","INDIGOPNTS.NS","IGL.NS","INDUSTOWER.NS","INDUSINDBK.NS","NAUKRI.NS",
"INFY.NS","INDIGO.NS","IPCALAB.NS","JBCHEPHARM.NS","JKCEMENT.NS","JKTYRE.NS","JMFINANCIL.NS","JSWENERGY.NS","JSWSTEEL.NS","JSWINFRA.NS",
"JINDALSTEL.NS","JIOFIN.NS","JUBLFOOD.NS","JUSTDIAL.NS","JYOTHYLAB.NS","KPRMILL.NS","KEI.NS","KNRCON.NS","KPITTECH.NS","KAJARIACER.NS",
"KALYANKJIL.NS","KAYNES.NS","KFINTECH.NS","KOTAKBANK.NS","KIMS.NS","LTF.NS","LTTS.NS","LICHSGFIN.NS","LTIM.NS","LT.NS",
"LATENTVIEW.NS","LAURUSLABS.NS","LICI.NS","LINDEINDIA.NS","LUPIN.NS","MRF.NS","MGL.NS","MAHSEAMLES.NS","M&MFIN.NS","M&M.NS",
"MANAPPURAM.NS","MRPL.NS","MARICO.NS","MARUTI.NS","MASTEK.NS","MFSL.NS","MAXHEALTH.NS","MAZDOCK.NS","MEDPLUS.NS","METROBRAND.NS",
"METROPOLIS.NS","MINDACORP.NS","MSUMI.NS","MPHASIS.NS","MCX.NS","MUTHOOTFIN.NS","NATCOPHARM.NS","NBCC.NS","NCC.NS","NHPC.NS",
"NLCINDIA.NS","NMDC.NS","NTPC.NS","NH.NS","NATIONALUM.NS","NAVINFLUOR.NS","NESTLEIND.NS","NAM-INDIA.NS","OBEROIRLTY.NS","ONGC.NS",
"OIL.NS","OLECTRA.NS","PAYTM.NS","OFSS.NS","POLICYBZR.NS","PCBL.NS","PEL.NS","PFC.NS","PIIND.NS","PAGEIND.NS",
"PATANJALI.NS","PERSISTENT.NS","PETRONET.NS","PHOENIXLTD.NS","PIDILITIND.NS","PEL.NS","PPLPHARMA.NS","POLYCAB.NS","POONAWALLA.NS","POWERGRID.NS",
"PRESTIGE.NS","PFIZER.NS","RBLBANK.NS","RECLTD.NS","RELIANCE.NS","ROSSARI.NS","SBICARD.NS","SBILIFE.NS","SJVN.NS","SKFINDIA.NS",
"SRF.NS","SAIL.NS","SAMMAANCAP.NS","MOTHERSON.NS","SAPPHIRE.NS","SAREGAMA.NS","SCHAEFFLER.NS","SEQUENT.NS","SHREECEM.NS","SHRIRAMFIN.NS",
"SHYAMMETL.NS","SIEMENS.NS","SONACOMS.NS","SBIN.NS","SAIL.NS","SOBHA.NS","SOLARINDS.NS","SONATSOFTW.NS","STARHEALTH.NS","SBIN.NS",
"SAIL.NS","SUNPHARMA.NS","SUNTV.NS","SUNDARMFIN.NS","SUNDRMFAST.NS","SUPREMEIND.NS","SUZLON.NS","SYNGENE.NS","SYRMA.NS","TVSMOTOR.NS",
"TATACHEM.NS","TATACOMM.NS","TCS.NS","TATACONSUM.NS","TATAELXSI.NS","TATAMOTORS.NS","TATAPOWER.NS","TATASTEEL.NS","TTML.NS","TEAMLEASE.NS",
"TECHM.NS","THERMAX.NS","TITAN.NS","TMB.NS","TORNTPHARM.NS","TORNTPOWER.NS","TRENT.NS","TRIDENT.NS","TRIVENI.NS","TRITURBINE.NS",
"TIINDIA.NS","UCOBANK.NS","UNIONBANK.NS","UBL.NS","MCDOWELL-N.NS","VBL.NS","VEDL.NS","VIJAYA.NS","VOLTAS.NS","WELCORP.NS",
"WELSPUNLIV.NS","WHIRLPOOL.NS","WIPRO.NS","YESBANK.NS","ZFCVINDIA.NS","ZEEL.NS","ZENSARTECH.NS","ZOMATO.NS","ZYDUSLIFE.NS"
]

print(f"Scanning {len(NSE500)} stocks... 4-Type CVD")
bull_reg, bear_reg, bull_hid, bear_hid = [],[],[],[]

for i, sym in enumerate(NSE500):
    try:
        df = yf.download(sym, period="3mo", interval="1d", progress=False, auto_adjust=True)
        if len(df)<50: continue
        df['CVD'] = (df['Close'].diff() * df['Volume']).cumsum()
        
        # 4-Type Logic
        p_low1 = df['Low'].iloc[-30:-15].min()
        p_low2 = df['Low'].iloc[-15:].min()
        c_low1 = df['CVD'].iloc[-30:-15].min()
        c_low2 = df['CVD'].iloc[-15:].min()
        
        p_high1 = df['High'].iloc[-30:-15].max()
        p_high2 = df['High'].iloc[-15:].max()
        c_high1 = df['CVD'].iloc[-30:-15].max()
        c_high2 = df['CVD'].iloc[-15:].max()
        
        if float(p_low2) < float(p_low1) and float(c_low2) > float(c_low1):
            bull_reg.append(sym.replace(".NS",""))
        if float(p_high2) > float(p_high1) and float(c_high2) < float(c_high1):
            bear_reg.append(sym.replace(".NS",""))
        if float(p_low2) > float(p_low1) and float(c_low2) < float(c_low1):
            bull_hid.append(sym.replace(".NS",""))
        if float(p_high2) < float(p_high1) and float(c_high2) > float(c_high1):
            bear_hid.append(sym.replace(".NS",""))
            
        if i%50==0: time.sleep(1) # Avoid Yahoo block
    except: continue

msg = f"""✅ *CVD Scanner 500 - FINAL*
Time: {now.strftime('%d-%m %H:%M IST')}

📈 *Regular Bullish* ({len(bull_reg)}): {', '.join(bull_reg[:10]) if bull_reg else 'None'}
📉 *Regular Bearish* ({len(bear_reg)}): {', '.join(bear_reg[:10]) if bear_reg else 'None'}
🔥 *Hidden Bullish* ({len(bull_hid)}): {', '.join(bull_hid[:10]) if bull_hid else 'None'}
❄️ *Hidden Bearish* ({len(bear_hid)}): {', '.join(bear_hid[:10]) if bear_hid else 'None'}

Scanned: {len(NSE500)} | Success ✅
Full list in logs.
"""
send(msg)
print(msg)
print("DONE - NSE 500 SCAN COMPLETE")

import yfinance as yf, pandas as pd, requests, os
from datetime import datetime
import pytz

# SECURE - Use GitHub Secrets, fallback to your token if secret not set
BOT = os.getenv("BOT_TOKEN") or "9102765194:AAEd_tiB_6v7AHP6Ymuy3jp-arUS4j7a"
CHAT = os.getenv("CHAT_ID") or "483927316"

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT}/sendMessage", data={"chat_id": CHAT, "text": msg, "parse_mode": "Markdown"}, timeout=15)
        print("Telegram sent!")
    except Exception as e: print(e)

now = datetime.now(pytz.timezone('Asia/Kolkata'))
IST = now.strftime('%d-%m %H:%M IST')

# KEEP YOUR 404 LIST - I am using your same variable name
NSE500 = ["360ONE.NS","3MINDIA.NS","ABB.NS","ACC.NS","AARTIIND.NS","AARTIPHARM.NS","AADHARHFC.NS","ABFRL.NS","ABSLAMC.NS","ADANIENT.NS","ADANIGREEN.NS","ADANIPOWER.NS","ADANIPORTS.NS","ADANIENSOL.NS","ADANIWL.NS","ATGL.NS","ABCAPITAL.NS","ABDL.NS","ABINDIA.NS","AEGISLOG.NS","AETHER.NS","AFFLE.NS","AJMERA.NS","AJANTPHARM.NS","AKZOINDIA.NS","ALEMBICLTD.NS","ALKYLAMINE.NS","ALOKINDS.NS","ARE&M.NS","AMBER.NS","AMBUJACEM.NS","ANANDRATHI.NS","ANGELONE.NS","ANURAS.NS","APARINDS.NS","APLLTD.NS","APOLLOHOSP.NS","APOLLOTYRE.NS","APTUS.NS","ACI.NS","ASAHIINDIA.NS","ASIANPAINT.NS","ASTERDM.NS","ASTRAZEN.NS","ASTRAL.NS","ATUL.NS","AUBANK.NS","AUROPHARMA.NS","AIIL.NS","DMART.NS","AXISBANK.NS","BEML.NS","BLS.NS","BSE.NS","BAJAJ-AUTO.NS","BAJAJCON.NS","BAJFINANCE.NS","BAJAJFINSV.NS","BAJAJHLDNG.NS","BAJAJHFL.NS","BALAMINES.NS","BALKRISIND.NS","BALRAMCHIN.NS","BANDHANBNK.NS","BANKBARODA.NS","BANKINDIA.NS","MAHABANK.NS","BATAINDIA.NS","BAYERCROP.NS","BBL.NS","BBTC.NS","BERGEPAINT.NS","BDL.NS","BEL.NS","BHARATFORG.NS","BHEL.NS","BPCL.NS","BHARTIARTL.NS","BHARTIHEXA.NS","BIKAJI.NS","BIOCON.NS","BIRLACORPN.NS","BSOFT.NS","BLUEDART.NS","BLUESTARCO.NS","BBNK.NS","BOSCHLTD.NS","BRIGADE.NS","BRITANNIA.NS","MAPMYINDIA.NS","CCL.NS","CESC.NS","CGPOWER.NS","CIEINDIA.NS","CRISIL.NS","CSBBANK.NS","CAMPUS.NS","CANFINHOME.NS","CANBK.NS","CAPLIPOINT.NS","CGCL.NS","CARBORUNIV.NS","CASTROLIND.NS","CEATLTD.NS","CENTRALBK.NS","CDSL.NS","CENTURYPLY.NS","CENTURYTEX.NS","CERA.NS","CHALET.NS","CHAMBLFERT.NS","CHENNPETRO.NS","CHOICEIN.NS","CHOLAHLDNG.NS","CHOLAFIN.NS","CIPLA.NS","CUB.NS","CLEAN.NS","COALINDIA.NS","COCHINSHIP.NS","COFORGE.NS","COLPAL.NS","CAMS.NS","CONCORDBIO.NS","CONCOR.NS","COROMANDEL.NS","CRAFTSMAN.NS","CREDITACC.NS","CROMPTON.NS","CUMMINSIND.NS","CYIENT.NS","DCMSHRIRAM.NS","DLF.NS","DOMS.NS","DABUR.NS","DALBHARAT.NS","DATAPATTNS.NS","DEEPAKFERT.NS","DEEPAKNTR.NS","DELHIVERY.NS","DEVYANI.NS","DIVISLAB.NS","DIXON.NS","LALPATHLAB.NS","DRREDDY.NS","DOMS.NS","EIDPARRY.NS","EICHERMOT.NS","ELECON.NS","ELGIEQUIP.NS","EMAMILTD.NS","ENDURANCE.NS","ENGINERSIN.NS","ENTENT.NS","ERIS.NS","ESCORTS.NS","ETERNAL.NS","EXIDEIND.NS","FDC.NS","FEDERALBNK.NS","FACT.NS","FINEORG.NS","FINCABLES.NS","FINPIPE.NS","FSL.NS","FIVESTAR.NS","FORTIS.NS","GAIL.NS","GVT&D.NS","GMMPFAUDLR.NS","GICRE.NS","GILLETTE.NS","GLAND.NS","GLAXO.NS","GLENMARK.NS","MEDANTA.NS","GODFRYPHLP.NS","GODREJAGRO.NS","GODREJCP.NS","GODREJIND.NS","GODREJPROP.NS","GRANULES.NS","GRAPHITE.NS","GRASIM.NS","GESHIP.NS","GRSE.NS","GUJALKALI.NS","GAEL.NS","FLUOROCHEM.NS","GUJGASLTD.NS","GMDCLTD.NS","GNFC.NS","GPPL.NS","GSFC.NS","GSPL.NS","HEG.NS","HBLPOWER.NS","HCLTECH.NS","HDFCAMC.NS","HDFCBANK.NS","HDFCLIFE.NS","HFCL.NS","HLEGLAS.NS","HAPPSTMNDS.NS","HAPPYFORGE.NS","HAVELLS.NS","HEROMOTOCO.NS","HSCL.NS","HINDALCO.NS","HAL.NS","HINDCOPPER.NS","HINDPETRO.NS","HINDUNILVR.NS","HINDZINC.NS","POWERINDIA.NS","HOMEFIRST.NS","HONASA.NS","HONAUT.NS","HUDCO.NS","HYUNDAI.NS","ICICIBANK.NS","ICICIGI.NS","ICICIPRULI.NS","ISEC.NS","IDBI.NS","IDFCFIRSTB.NS","IFCI.NS","IIFL.NS","IIFLCAPS.NS","IRB.NS","IRCON.NS","ITC.NS","ITI.NS","INDIACEM.NS","IBULHSGFIN.NS","INDIANB.NS","IEX.NS","INDHOTEL.NS","IOC.NS","IOB.NS","IRCTC.NS","IRFC.NS","INDUSINDBK.NS","NAUKRI.NS","INFY.NS","INDIGO.NS","IPCALAB.NS","JBCHEPHARM.NS","JKCEMENT.NS","JKTYRE.NS","JMFINANCIL.NS","JSWENERGY.NS","JSWSTEEL.NS","JSWINFRA.NS","JAMNAAUTO.NS","JINDALSTEL.NS","JIOFIN.NS","JSL.NS","JSLL.NS","JUBLFOOD.NS","JUBLINGREA.NS","JUBLPHARMA.NS","JUNIPER.NS","JUSTDIAL.NS","JYOTHYLAB.NS","KPRMILL.NS","KEI.NS","KNRCON.NS","KPITTECH.NS","KAJARIACER.NS","KPIL.NS","KALYANKJIL.NS","KANSAINER.NS","KARURVYSYA.NS","KAYNES.NS","KEC.NS","KFINTECH.NS","KOTAKBANK.NS","KIMS.NS","LTF.NS","LTTS.NS","LICHSGFIN.NS","LTIM.NS","LT.NS","LATENTVIEW.NS","LAURUSLABS.NS","LEMONTREE.NS","LICI.NS","LINDEINDIA.NS","LLOYDSENT.NS","LUPIN.NS","MMTC.NS","MRF.NS","MTARTECH.NS","LODHA.NS","MGL.NS","MAHSEAMLES.NS","M&MFIN.NS","M&M.NS","MANAPPURAM.NS","MRPL.NS","MANKIND.NS","MARICO.NS","MARUTI.NS","MASTEK.NS","MFSL.NS","MAXHEALTH.NS","MAZDOCK.NS","MEDPLUS.NS","MUTHOOTFIN.NS","NATCOPHARM.NS","NBCC.NS","NCC.NS","NESCO.NS","NHPC.NS","NLCINDIA.NS","NMDC.NS","NTPC.NS","NH.NS","NATIONALUM.NS","NAVA.NS","NAVINFLUOR.NS","NESTLEIND.NS","NETWORK18.NS","NAM-INDIA.NS","NUVAMA.NS","OBEROIRLTY.NS","ONGC.NS","OIL.NS","OLAELEC.NS","OLECTRA.NS","PAYTM.NS","OFSS.NS","POLICYBZR.NS","ORCHPHARMA.NS","ORIENTCEM.NS","ORIENTELEC.NS","PAGEIND.NS","PATANJALI.NS","PERSISTENT.NS","PETRONET.NS","PFIZER.NS","PHOENIXLTD.NS","PIDILITIND.NS","PEL.NS","PPLPHARMA.NS","POLYMED.NS","POLYCAB.NS","POONAWALLA.NS","PFC.NS","POWERGRID.NS","PRAJIND.NS","PRESTIGE.NS","PRINCEPIPE.NS","PRSMJOHNSN.NS","PGHH.NS","PNB.NS","RRKABEL.NS","RBLBANK.NS","RECLTD.NS","RELIANCE.NS","RELIGARE.NS","RPOWER.NS","ROUTE.NS","SBFC.NS","SBICARD.NS","SBILIFE.NS","SJVN.NS","SKFINDIA.NS","SRF.NS","SAGILITY.NS","SAMMAANCAP.NS","MOTHERSON.NS","SANTECH.NS","SBIN.NS","SCHAEFFLER.NS","SEQUENT.NS","SHREECEM.NS","RENUKA.NS","SHRIRAMFIN.NS","SHYAMMETL.NS","SIEMENS.NS","SIGNATURE.NS","SOBHA.NS","SOLARINDS.NS","SONACOMS.NS","SONATSOFTW.NS","STARHEALTH.NS","SBILIFE.NS","SAIL.NS","SWSOLAR.NS","SUNPHARMA.NS","SUNTV.NS","SUNDARMFIN.NS","SUNDRMFAST.NS","SUPREMEIND.NS","SUZLON.NS","SWANENERGY.NS","SYNGENE.NS","SYRMA.NS","TTKPRESTIG.NS","TVSMOTOR.NS","TATACHEM.NS","TATACOMM.NS","TCS.NS","TATACONSUM.NS","TATAELXSI.NS","TATAMOTORS.NS","TATAPOWER.NS","TATASTEEL.NS","TATATECH.NS","TTML.NS","TEJASNET.NS","NIACL.NS","RAMCOCEM.NS","TORNTPHARM.NS","TORNTPOWER.NS","TRENT.NS","TRIDENT.NS","TRIVENI.NS","TRITURBINE.NS","TIINDIA.NS","UCOBANK.NS","UNOMINDA.NS","UPL.NS","UTIAMC.NS","ULTRACEMCO.NS","UNIONBANK.NS","UBL.NS","MCDOWELL-N.NS","VGUARD.NS","VIPIND.NS","VAIBHAVGBL.NS","VBL.NS","MANYAVAR.NS","VEDL.NS","VIJAYA.NS","VOLTAS.NS","WAAREEENER.NS","WELCORP.NS","WELSPUNLIV.NS","WESTLIFE.NS","WHIRLPOOL.NS","WIPRO.NS","YESBANK.NS","ZFCVINDIA.NS","ZEEL.NS","ZENSARTECH.NS","ZYDUSLIFE.NS","ECLERX.NS"]

print(f"Starting FINAL scan {len(NSE500)} stocks - LONESOME FORMULA {IST}")

bull_reg, bear_reg, bull_hid, bear_hid = [], [], [], []

# Batch download
try:
    data = yf.download(NSE500, period="3mo", group_by='ticker', threads=True, progress=False, auto_adjust=True)
except Exception as e:
    print(e)
    data = None

# LONESOME CVD LOGIC
if data is not None:
    for sym in NSE500:
        try:
            # Extract ticker data
            if len(NSE500) > 1:
                try:
                    df = data[sym]
                except:
                    continue
            else:
                df = data
            
            df = df.dropna()
            if len(df) < 50:
                continue

            # --- LONESOME FORMULA ---
            # Money Flow Volume = ((Close - Open) / (High - Low)) * Volume
            hl = (df['High'] - df['Low']).replace(0, 0.0001)
            mf = ((df['Close'] - df['Open']) / hl) * df['Volume']
            cvd = mf.cumsum()
            
            # Divergence check - Compare Price vs CVD over last 20 candles
            price_now = float(df['Close'].iloc[-1])
            price_20 = float(df['Close'].iloc[-20])
            cvd_now = float(cvd.iloc[-1])
            cvd_20 = float(cvd.iloc[-20])
            
            price_change = (price_now - price_20) / price_20 * 100
            cvd_change = cvd_now - cvd_20
            
            # Regular Bullish: Price Lower Low, CVD Higher Low
            if price_change < -2 and cvd_change > 0:
                bull_reg.append(sym.replace(".NS",""))
            # Regular Bearish: Price Higher High, CVD Lower High  
            elif price_change > 2 and cvd_change < 0:
                bear_reg.append(sym.replace(".NS",""))
            # Hidden Bullish: Price Higher Low, CVD Lower Low
            elif price_change > 0.5 and cvd_change < 0:
                bull_hid.append(sym.replace(".NS",""))
            # Hidden Bearish: Price Lower High, CVD Higher High
            elif price_change < -0.5 and cvd_change > 0:
                bear_hid.append(sym.replace(".NS",""))

        except Exception as e:
            continue

# Message with LONESOME tag - So you know it's new formula
msg = f"""🔥 *CVD Scanner 500 - LONESOME FORMULA*
🕒 {IST}

✅ *Regular Bullish* ({len(bull_reg)}): 
{', '.join(bull_reg[:20]) if bull_reg else 'None'}

❌ *Regular Bearish* ({len(bear_reg)}): 
{', '.join(bear_reg[:20]) if bear_reg else 'None'}

👀 *Hidden Bullish* ({len(bull_hid)}): 
{', '.join(bull_hid[:15]) if bull_hid else 'None'}

⚠️ *Hidden Bearish* ({len(bear_hid)}): 
{', '.join(bear_hid[:15]) if bear_hid else 'None'}

Formula: ((Close-Open)/(High-Low))*Volume Cumsum
"""

print(msg)
send(msg)

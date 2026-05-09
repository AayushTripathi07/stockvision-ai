import pandas as pd
import requests
import os
import ssl
from io import StringIO

def get_ticker_list():
    """
    Fetches a massive list of global tickers including the full NSE (India) master list.
    """
    cache_path = "app/data/tickers_cache.csv"
    
    if os.path.exists(cache_path):
        try:
            return pd.read_csv(cache_path)["Ticker"].tolist()
        except:
            pass
            
    tickers = []
    headers = {"User-Agent": "Mozilla/5.0"}
    ssl._create_default_https_context = ssl._create_unverified_context
    
    # 1. FULL INDIAN MARKET (NSE Master List)
    try:
        # Official NSE Equity Master List
        url_nse = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
        resp = requests.get(url_nse, headers=headers)
        if resp.status_code == 200:
            df_nse = pd.read_csv(StringIO(resp.text))
            if 'SYMBOL' in df_nse.columns:
                # Add .NS suffix for NSE stocks
                tickers.extend([f"{s}.NS" for s in df_nse['SYMBOL']])
    except Exception as e:
        print(f"Error fetching full NSE list: {e}")

    # 2. US: S&P 500
    try:
        url_sp500 = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        resp_sp = requests.get(url_sp500, headers=headers)
        df_sp = pd.read_html(StringIO(resp_sp.text))[0]
        # For US stocks, replace dot with hyphen (e.g. BRK.B -> BRK-B)
        tickers.extend([s.replace('.', '-') for s in df_sp['Symbol'].tolist()])
    except: pass
    
    # 3. GLOBAL MAJORS & INDICES
    tickers.extend([
        "TSLA", "NVDA", "AAPL", "MSFT", "GOOGL", "BTC-USD", "ETH-USD",
        "^NSEI", "^BSESN", "^GSPC", "^FTSE", "^N225"
    ])

    # Clean and sort - AVOID global . replacement to preserve .NS suffix
    cleaned_tickers = []
    for t in tickers:
        if not t: continue
        t_str = str(t).strip().upper()
        if len(t_str) < 15 and ' ' not in t_str:
            cleaned_tickers.append(t_str)
            
    tickers = sorted(list(set(cleaned_tickers)))
    
    if len(tickers) < 100: # Emergency Fallback
        tickers = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "AAPL", "TSLA", "NVDA"]

    pd.DataFrame({"Ticker": tickers}).to_csv(cache_path, index=False)
    return tickers

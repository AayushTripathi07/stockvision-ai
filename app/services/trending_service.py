import yfinance as yf
import pandas as pd

class TrendingService:
    def __init__(self):
        self.popular_us = [
            "NVDA", "AAPL", "TSLA", "AMZN", "MSFT", "GOOGL", "META", "NFLX", "AMD", "PLTR",
            "AVGO", "ORCL", "SMCI", "COIN", "MARA", "MSTR", "AMD", "BABA", "NIO", "PYPL"
        ]
        self.popular_in = [
            "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", 
            "TATAMOTORS.NS", "ADANIENT.NS", "SBIN.NS", "BHARTIARTL.NS", "ZOMATO.NS",
            "ITC.NS", "HINDUNILVR.NS", "LT.NS", "AXISBANK.NS", "BAJFINANCE.NS",
            "MARUTI.NS", "SUNPHARMA.NS", "TATASTEEL.NS", "WIPRO.NS", "TITAN.NS"
        ]

    def fetch_trending(self, region="US"):
        """
        Fetches trending stocks for a specific region.
        """
        tickers = self.popular_us if region == "US" else self.popular_in
        results = []
        
        for ticker in tickers:
            try:
                t = yf.Ticker(ticker)
                fast = t.fast_info
                lp = fast.last_price
                pc = fast.previous_close
                if lp and pc:
                    change = ((lp - pc) / pc) * 100
                    results.append({
                        "symbol": ticker.replace(".NS", ""),
                        "price": lp,
                        "change": change
                    })
            except:
                continue
        
        return sorted(results, key=lambda x: abs(x['change']), reverse=True)

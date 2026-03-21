import os
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import Fundamentals

class AlphaVantageService:
    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.ts = TimeSeries(key=self.api_key, output_format='pandas') if self.api_key else None
        self.fd = Fundamentals(key=self.api_key) if self.api_key else None

    def get_global_sentiment(self, ticker: str):
        """
        Alpha Vantage provides a specialized 'News Sentiment' endpoint for global stocks.
        """
        if not self.api_key:
            return None
        
        # This uses the news_sentiment endpoint which is unique to AV
        try:
            import requests
            url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={self.api_key}'
            r = requests.get(url)
            data = r.json()
            return data.get('feed', [])[:5]
        except:
            return None

    def get_earnings_calendar(self, ticker: str):
        """
        Fetches upcoming earnings dates for global companies.
        """
        if not self.fd:
            return None
        try:
            earnings, _ = self.fd.get_earnings(symbol=ticker)
            return earnings.head(5)
        except:
            return None

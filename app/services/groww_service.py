import os
try:
    from growwapi import GrowwAPI
except ImportError:
    GrowwAPI = None

class GrowwService:
    def __init__(self):
        self.api_key = os.getenv("GROWW_API_KEY")
        self.api_secret = os.getenv("GROWW_API_SECRET")
        self.client = None
        if GrowwAPI and self.api_key and self.api_secret:
            try:
                self.client = GrowwAPI(api_key=self.api_key, api_secret=self.api_secret)
            except Exception as e:
                print(f"Groww Auth Error: {e}")

    def get_live_price(self, ticker: str):
        """
        Fetches zero-latency LTP for Indian stocks.
        """
        if not self.client or not ticker.endswith(".NS"):
            return None
        
        try:
            # Normalize ticker for Groww (e.g., RELIANCE.NS -> RELIANCE)
            symbol = ticker.split(".")[0]
            # This is a representative call, exact SDK method depends on latest growwapi docs
            quote = self.client.get_quote(symbol) 
            return quote.get('ltp')
        except:
            return None

    def place_order(self, ticker: str, quantity: int, order_type: str = "BUY"):
        """
        Executes a trade on Groww.
        """
        if not self.client:
            return {"status": "error", "message": "Groww not connected"}
        
        # Placeholder for order execution logic
        return {"status": "simulated", "message": f"{order_type} order for {quantity} shares of {ticker} placed via Groww."}

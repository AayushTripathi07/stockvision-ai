from app.features.technical_indicators import add_technical_indicators
import pandas as pd

class AlertService:
    def check_alerts(self, df: pd.DataFrame, ticker: str) -> list:
        """
        Scans technical indicators for intraday alert conditions.
        """
        if df.empty:
            return []
            
        alerts = []
        try:
            # Ensure indicators are present
            df_tech = add_technical_indicators(df)
            latest = df_tech.iloc[-1]
            
            rsi = latest.get("RSI", 50)
            price = latest.get("Close", 0)
            sma = latest.get("SMA_20", 0)
            bb_high = latest.get("BB_high", 0)
            bb_low = latest.get("BB_low", 0)

            # 1. RSI Extremes
            if rsi > 75:
                alerts.append({"type": "DANGER", "msg": f"RSI Overbought ({rsi:.1f}) - Potential Reversal"})
            elif rsi < 25:
                alerts.append({"type": "OPPORTUNITY", "msg": f"RSI Oversold ({rsi:.1f}) - Accumulation Zone"})

            # 2. Bollinger Band Breakouts
            if price > bb_high:
                alerts.append({"type": "VOLATILITY", "msg": "Price broken above upper Bollinger Band"})
            elif price < bb_low:
                alerts.append({"type": "VOLATILITY", "msg": "Price dropped below lower Bollinger Band"})

            # 3. SMA Cross (Golden/Death Cross simplified)
            if price > sma * 1.05:
                alerts.append({"type": "BULLISH", "msg": "Trading significantly above 20-day SMA"})
            elif price < sma * 0.95:
                alerts.append({"type": "BEARISH", "msg": "Price slipped 5% below 20-day SMA"})

        except Exception as e:
            print(f"Alert Scan Error for {ticker}: {e}")
            
        return alerts

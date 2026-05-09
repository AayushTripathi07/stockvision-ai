class IntelligenceService:
    def evaluate_signals(self, price_predictions: dict, sentiment_data: dict, current_price: float) -> dict:
        """
        Fuses price predictions and sentiment to generate actionable intelligence.
        """
        ensemble_pred = price_predictions["ensemble"]
        price_change_pct = ((ensemble_pred - current_price) / current_price) * 100
        
        sentiment_score = sentiment_data["score"]
        
        # Simple Logic for Signal
        # Bullish if both predict upward trend or strong upward + neutral
        signal = "HOLD"
        confidence = 50.0 # Base confidence
        risk = "MEDIUM"
        
        if price_change_pct > 1.0 and sentiment_score > 0.1:
            signal = "BUY"
            confidence += min(price_change_pct * 5 + sentiment_score * 20, 45)
            risk = "LOW" if sentiment_score > 0.5 else "MEDIUM"
        elif price_change_pct < -1.0 and sentiment_score < -0.1:
            signal = "SELL"
            confidence += min(abs(price_change_pct) * 5 + abs(sentiment_score) * 20, 45)
            risk = "HIGH"
        elif price_change_pct > 2.0:
            signal = "BUY"
            confidence += 10
            risk = "HIGH" # High price jump but no sentiment backup
        elif price_change_pct < -2.0:
            signal = "SELL"
            confidence += 10
            risk = "HIGH"
            
        return {
            "signal": signal,
            "confidence": round(min(confidence, 99.9), 2),
            "risk_level": risk,
            "expected_price_change_pct": round(price_change_pct, 2)
        }
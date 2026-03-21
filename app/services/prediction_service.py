from app.data.market_data import fetch_stock_data
from app.models.arima_model import train_arima, predict_arima
from app.models.lstm_model import train_lstm, predict_lstm
from app.models.transformer_model import train_transformer, predict_transformer
from app.models.ensemble_model import EnsembleModel
from app.data.news_data import fetch_stock_news
from app.sentiment.sentiment_analyzer import SentimentAnalyzer
from app.services.intelligence_service import IntelligenceService
from app.agents.financial_agent import generate_explanation, conduct_research_debate, decode_executive_tone
from app.features.technical_indicators import add_technical_indicators
from app.services.social_service import SocialService
from app.services.alert_service import AlertService
import yfinance as yf

class PredictionService:
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.intelligence_service = IntelligenceService()
        self.social_service = SocialService()
        self.alert_service = AlertService()

    def predict_stock(self, ticker):
        print(f"Fetching market data for {ticker}...")
        data_bundle = fetch_stock_data(ticker)
        df = data_bundle["df"]
        fundamentals = data_bundle["fundamentals"]
        
        # Add Quantitative Indicators
        df_with_tech = add_technical_indicators(df)
        latest_tech = {
            "rsi": float(df_with_tech["RSI"].iloc[-1]),
            "macd": float(df_with_tech["MACD"].iloc[-1]),
            "macd_signal": float(df_with_tech["MACD_signal"].iloc[-1]),
            "sma_20": float(df_with_tech["SMA_20"].iloc[-1]),
            "bb_high": float(df_with_tech["BB_high"].iloc[-1]),
            "bb_low": float(df_with_tech["BB_low"].iloc[-1]),
            "volatility": float(df_with_tech["volatility"].iloc[-1])
        }
        
        # Institutional & Major Holders (Global Support)
        institutional_holders = []
        try:
            t = yf.Ticker(ticker)
            
            # 1. Try institutional_holders (US primarily)
            holders = t.institutional_holders
            if holders is not None and not holders.empty:
                # Convert to standard format
                institutional_holders = holders.head(10).to_dict('records')
            
            # 2. Fallback to major_holders (India/Global)
            if not institutional_holders:
                major = t.major_holders
                if major is not None and not major.empty:
                    # Convert breakdown table to a list of dicts for universal UI
                    # Usually: [Value, Breakdown] or [Breakdown, Value]
                    institutional_holders = [{"Holder": str(row[0]), "Value": str(row[1])} for row in major.values]
        except Exception as e:
            print(f"Holder Fetch Error for {ticker}: {e}")

        current_price = float(df["Close"].iloc[-1])

        # Model Predictions
        print("Running ARIMA...")
        arima_model = train_arima(df["Close"])
        arima_pred = predict_arima(arima_model)

        print("Running LSTM...")
        lstm_model, scaler = train_lstm(df["Close"])
        lstm_pred = predict_lstm(lstm_model, scaler, df["Close"])

        print("Running Transformer...")
        transformer_model = train_transformer(df)
        transformer_pred = predict_transformer(transformer_model, df)

        print("Running Ensemble...")
        ensemble = EnsembleModel()
        ensemble.train(
            [arima_pred],
            [lstm_pred],
            [transformer_pred],
            [current_price]
        )

        final_pred = ensemble.predict(
            arima_pred,
            lstm_pred,
            transformer_pred
        )
        
        predictions = {
            "arima": float(arima_pred),
            "lstm": float(lstm_pred),
            "transformer": float(transformer_pred),
            "ensemble": float(final_pred[0])
        }

        # News & Sentiment Analysis
        print("Fetching news and analyzing sentiment...")
        news_items = fetch_stock_news(ticker, limit=15)
        sentiment_data = self.sentiment_analyzer.analyze_news(news_items)

        # Social Hype Tracking
        print("Scanning Social Intelligence (Reddit)...")
        social_data = self.social_service.fetch_reddit_hype(ticker)

        # Intelligence Layer
        print("Generating intelligence signals...")
        intelligence_data = self.intelligence_service.evaluate_signals(
            price_predictions=predictions,
            sentiment_data=sentiment_data,
            current_price=current_price
        )

        # Intraday Alerts
        alerts = self.alert_service.check_alerts(df, ticker)
        
        analysis_data = {
            "current_price": current_price,
            "predictions": predictions,
            "sentiment": sentiment_data,
            "social": social_data,
            "intelligence": intelligence_data,
            "recent_news": news_items,
            "fundamentals": fundamentals,
            "technicals": latest_tech,
            "alerts": alerts,
            "institutional_holders": institutional_holders
        }

        # Billion Dollar GenAI Layer
        print(f"Conducting Research Debate for {ticker}...")
        try:
            debate = conduct_research_debate(ticker, analysis_data)
            analysis_data["debate"] = debate
        except Exception as e:
            analysis_data["debate"] = {"error": str(e)}

        print(f"Decoding Executive Tone for {ticker}...")
        try:
            exec_tone = decode_executive_tone(ticker, news_items)
            analysis_data["executive_tone"] = exec_tone
        except Exception as e:
            analysis_data["executive_tone"] = f"Tone analysis unavailable: {e}"

        # GenAI Explanation
        print("Generating explanation...")
        explanation = generate_explanation(ticker, analysis_data)
        analysis_data["explanation"] = explanation

        return analysis_data

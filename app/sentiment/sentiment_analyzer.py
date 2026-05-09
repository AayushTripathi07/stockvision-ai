from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        # Using FinBERT for financial text sentiment analysis
        self.analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")
        
    def analyze_news(self, news_items: list) -> dict:
        """
        Analyzes a list of news items and returns an aggregated sentiment score.
        Scores range roughly from -1 (very negative) to 1 (very positive).
        """
        if not news_items:
            return {"sentiment": "neutral", "score": 0.0, "details": []}
            
        texts = [item["title"] for item in news_items]
        results = self.analyzer(texts)
        
        total_score = 0.0
        for res in results:
            label = res["label"]
            score = res["score"]
            if label == "positive":
                total_score += score
            elif label == "negative":
                total_score -= score
                
        avg_score = total_score / len(news_items)
        
        sentiment = "neutral"
        if avg_score > 0.2:
            sentiment = "positive"
        elif avg_score < -0.2:
            sentiment = "negative"
            
        return {
            "sentiment": sentiment,
            "score": round(avg_score, 4),
            "details": results
        }
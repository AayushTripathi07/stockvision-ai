import requests
import time
from app.sentiment.sentiment_analyzer import SentimentAnalyzer

class SocialService:
    def __init__(self):
        self.analyzer = SentimentAnalyzer()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.subreddits = [
            "wallstreetbets", "stocks", "investing", "stockmarket", 
            "IndianStreetBets", "IndiaInvestments", "pennystocks"
        ]

    def fetch_reddit_hype(self, ticker: str) -> dict:
        """
        Scans multiple subreddits for mentions of the ticker and analyzes sentiment.
        """
        all_posts = []
        ticker_upper = ticker.upper().replace(".NS", "").replace(".BO", "")
        
        for sub in self.subreddits:
            try:
                url = f"https://www.reddit.com/r/{sub}/search.json?q={ticker_upper}&sort=new&restrict_sr=on&t=week"
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get('data', {}).get('children', [])
                    for post in posts:
                        pdata = post.get('data', {})
                        all_posts.append({
                            "title": pdata.get('title'),
                            "subreddit": sub,
                            "ups": pdata.get('ups'),
                            "url": f"https://reddit.com{pdata.get('permalink')}"
                        })
                # Respect Reddit rate limits slightly
                time.sleep(0.1)
            except Exception as e:
                print(f"Error fetching from r/{sub}: {e}")

        if not all_posts:
            return {"hype_score": 0, "sentiment": "Neutral", "mention_count": 0, "top_posts": []}

        # Analyze sentiment of post titles
        titles = [p["title"] for p in all_posts[:20]] # Limit to top 20 for speed
        sentiment_res = self.analyzer.analyze_news([{"title": t} for t in titles])
        
        # Calculate Hype Score (based on mentions and upvotes)
        mention_count = len(all_posts)
        total_ups = sum([p["ups"] for p in all_posts])
        
        # Normalize score 0-100
        # Formula: (Mentions * 2) + (Upvotes / 10) capped at 100
        hype_score = min((mention_count * 5) + (total_ups / 50), 100)

        return {
            "hype_score": round(hype_score, 1),
            "sentiment": sentiment_res["sentiment"],
            "sentiment_score": sentiment_res["score"],
            "mention_count": mention_count,
            "top_posts": all_posts[:5] # Return top 5 posts
        }

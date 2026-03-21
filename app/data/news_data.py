import yfinance as yf

def fetch_stock_news(ticker: str, limit: int = 20) -> list:
    """
    Fetches real-time news for a given stock ticker using yfinance.
    Returns a list of dictionaries containing title, link, and published date.
    """
    stock = yf.Ticker(ticker)
    news_items = []
    
    try:
        news = stock.news
        if not news:
            return []
            
        for item in news[:limit]:
            content = item.get('content', {})
            title = content.get('title', 'No Title')
            
            link = ""
            canonical = content.get('clickThroughUrl', {})
            if isinstance(canonical, dict):
                link = canonical.get('url', '')
            elif isinstance(content.get('canonicalUrl'), dict):
                link = content.get('canonicalUrl').get('url', '')
                
            pubDate = content.get('pubDate', '')
            
            news_items.append({
                "title": title,
                "link": link,
                "published": pubDate
            })
    except Exception as e:
        print(f"Failed to fetch news for {ticker}: {e}")
        
    return news_items
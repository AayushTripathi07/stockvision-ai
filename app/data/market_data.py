import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker="AAPL", period="2y"):
    """
    Fetches historical stock data and comprehensive fundamental metrics.
    Returns a dictionary with 'df' (DataFrame) and 'fundamentals' (dict).
    """
    print(f"Downloading data for {ticker}...")
    
    stock = yf.Ticker(ticker)
    
    # 1. Historical Price Data
    df = stock.history(period=period, interval="1d", auto_adjust=True)
    
    if df is None or df.empty:
        raise ValueError("Stock data download failed. Try again or check ticker.")

    df.index = pd.to_datetime(df.index)
    df = df.ffill()

    # 2. Fundamental Intelligence - Expanded
    info = stock.info
    fundamentals = {
        "name": info.get("longName") or info.get("shortName") or ticker,
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "summary": info.get("longBusinessSummary", "No summary available."),
        "pe_ratio": info.get("forwardPE", "N/A"),
        "trailing_pe": info.get("trailingPE", "N/A"),
        "pb_ratio": info.get("priceToBook", "N/A"),
        "ps_ratio": info.get("priceToSalesTrailing12Months", "N/A"),
        "market_cap": info.get("marketCap", 0),
        "div_yield": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0,
        "revenue_growth": info.get("revenueGrowth", 0) * 100 if info.get("revenueGrowth") else 0,
        "profit_margins": info.get("profitMargins", 0) * 100 if info.get("profitMargins") else 0,
        "roe": info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else 0,
        "roa": info.get("returnOnAssets", 0) * 100 if info.get("returnOnAssets") else 0,
        "debt_to_equity": info.get("debtToEquity", "N/A"),
        "total_cash": info.get("totalCash", 0),
        "total_debt": info.get("totalDebt", 0),
        "operating_cash_flow": info.get("operatingCashflow", 0),
        "free_cash_flow": info.get("freeCashflow", 0),
        "ebitda": info.get("ebitda", 0),
        "current_ratio": info.get("currentRatio", "N/A"),
        "quick_ratio": info.get("quickRatio", "N/A"),
        "book_value": info.get("bookValue", 0),
        "ebitda_margins": info.get("ebitdaMargins", 0),
        "currency": info.get("currency", "USD")
    }

    print(f"Download finished for {ticker}")

    return {
        "df": df,
        "fundamentals": fundamentals
    }

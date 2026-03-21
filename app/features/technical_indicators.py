import pandas as pd
import ta


def add_technical_indicators(df):

    df = df.copy()

    # Force Close column to be a 1D pandas Series
    close = df["Close"].values.ravel()
    close = pd.Series(close, index=df.index)

    # Returns
    df["return"] = close.pct_change()

    # Moving averages
    df["SMA_10"] = close.rolling(10).mean()
    df["SMA_20"] = close.rolling(20).mean()

    # RSI
    df["RSI"] = ta.momentum.RSIIndicator(close=close, window=14).rsi()

    # MACD
    macd = ta.trend.MACD(close=close)
    df["MACD"] = macd.macd()
    df["MACD_signal"] = macd.macd_signal()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(close=close)
    df["BB_high"] = bb.bollinger_hband()
    df["BB_low"] = bb.bollinger_lband()

    # Volatility
    df["volatility"] = df["return"].rolling(10).std()

    df = df.dropna()

    return df
from fastapi import FastAPI
from app.data.market_data import fetch_stock_data

app = FastAPI()

@app.get("/stock/{ticker}")

def get_stock(ticker: str):

    df = fetch_stock_data(ticker)

    return df.tail().to_dict()
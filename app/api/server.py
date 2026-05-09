from fastapi import FastAPI
from app.services.prediction_service import PredictionService
import traceback

app = FastAPI()

service = PredictionService()


@app.get("/predict/{ticker}")
def predict(ticker: str):
    try:
        result = service.predict_stock(ticker)
        return result

    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }
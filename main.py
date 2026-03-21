from app.data.market_data import fetch_stock_data
from app.features.feature_engineering import prepare_features
from app.models.arima_model import train_arima, predict_arima
from app.models.lstm_model import train_lstm, predict_lstm
from app.models.transformer_model import train_transformer, predict_transformer

from app.models.ensemble_model import EnsembleModel


print("Fetching stock data...")

df = fetch_stock_data("AAPL")

df = prepare_features(df)

print(df.columns)


# =========================
# ARIMA MODEL
# =========================

arima_model = train_arima(df["Close"])

arima_pred = predict_arima(arima_model)


# =========================
# LSTM MODEL
# =========================

lstm_model, scaler = train_lstm(df["Close"])

lstm_pred = predict_lstm(lstm_model, scaler, df["Close"])


# =========================
# TRANSFORMER MODEL
# =========================

transformer_model = train_transformer(df)

transformer_pred = predict_transformer(transformer_model, df)


# =========================
# PRINT INDIVIDUAL RESULTS
# =========================

print("ARIMA:", arima_pred)
print("LSTM:", lstm_pred)
print("Transformer:", transformer_pred)


# =========================
# ENSEMBLE MODEL
# =========================

ensemble = EnsembleModel()

# temporary training data example
ensemble.train(
    arima_preds=[arima_pred],
    lstm_preds=[lstm_pred],
    transformer_preds=[transformer_pred],
    actual=[df["Close"].iloc[-1]]
)

final_prediction = ensemble.predict(
    arima_pred,
    lstm_pred,
    transformer_pred
)

print("Final Ensemble Prediction:", final_prediction)
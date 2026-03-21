import numpy as np

class EnsembleModel:
    def __init__(self):
        # Weights for ARIMA, LSTM, Transformer
        self.weights = [0.2, 0.4, 0.4]

    def train(self, arima_preds, lstm_preds, transformer_preds, actual):
        # In a real scenario, we would use historical predictions to fit the weights.
        # Since we only have a single point currently, we use fixed weights to avoid overfitting.
        pass

    def predict(self, arima_pred, lstm_pred, transformer_pred):
        # Weighted average of the predictions
        ensemble_pred = (
            self.weights[0] * arima_pred +
            self.weights[1] * lstm_pred +
            self.weights[2] * transformer_pred
        )
        return [ensemble_pred]
import pandas as pd
import numpy as np
from neuralforecast import NeuralForecast
from neuralforecast.models import PatchTST


def train_transformer(df):

    prices = np.array(df["Close"]).flatten()

    data = pd.DataFrame({
        "unique_id": ["stock"] * len(prices),
        "ds": pd.to_datetime(df.index),
        "y": prices
    })

    model = PatchTST(
        h=1,
        input_size=60,
        patch_len=16,
        hidden_size=64,
        learning_rate=1e-3,
        max_steps=20
    )

    nf = NeuralForecast(
        models=[model],
        freq="D"
    )

    nf.fit(data)

    return nf


def predict_transformer(model, df):

    prices = np.array(df["Close"]).flatten()

    data = pd.DataFrame({
        "unique_id": ["stock"] * len(prices),
        "ds": pd.to_datetime(df.index),
        "y": prices
    })

    forecast = model.predict(data)

    return forecast["PatchTST"].iloc[-1]
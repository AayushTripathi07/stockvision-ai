import torch
import torch.nn as nn
import numpy as np
import torch 
from sklearn.preprocessing import MinMaxScaler


class LSTMModel(nn.Module):

    def __init__(self, input_size=1, hidden_size=64, num_layers=2):
        super(LSTMModel, self).__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True
        )

        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):

        # x shape -> (batch, seq_length, features)

        out, _ = self.lstm(x)

        # take output from last timestep
        out = out[:, -1, :]

        out = self.fc(out)

        return out


def create_sequences(data, seq_length):

    X = []
    y = []

    for i in range(len(data) - seq_length):

        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])

    X = np.array(X)
    y = np.array(y)

    return X, y


def train_lstm(series, seq_length=60, epochs=15):

    prices = series.values.reshape(-1, 1)

    scaler = MinMaxScaler()

    scaled_prices = scaler.fit_transform(prices)

    X, y = create_sequences(scaled_prices, seq_length)

    # reshape for LSTM (batch, seq_length, features)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    X = torch.tensor(X, dtype=torch.float32)
    y = torch.tensor(y, dtype=torch.float32)

    model = LSTMModel()

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    model.train()

    for epoch in range(epochs):

        outputs = model(X)

        loss = criterion(outputs.view(-1), y.view(-1))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 5 == 0:
            print(f"LSTM Epoch {epoch+1}/{epochs}, Loss: {loss.item():.6f}")

    return model, scaler


def predict_lstm(model, scaler, series, seq_length=60):

    model.eval()

    prices = series.values.reshape(-1, 1)

    scaled_prices = scaler.transform(prices)

    seq = scaled_prices[-seq_length:]

    seq = seq.reshape(1, seq_length, 1)

    seq = torch.tensor(seq, dtype=torch.float32)

    with torch.no_grad():

        prediction = model(seq).item()

    # inverse scale back to real price
    prediction = scaler.inverse_transform([[prediction]])

    return prediction[0][0]

def save_lstm(model, scaler):
    torch.save({
        "model_state": model.state_dict(),
        "scaler": scaler
    }, "models/lstm.pth")


def load_lstm(model_class):
    checkpoint = torch.load("models/lstm.pth")

    model = model_class()
    model.load_state_dict(checkpoint["model_state"])
    model.eval()

    scaler = checkpoint["scaler"]

    return model, scaler
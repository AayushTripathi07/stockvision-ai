from statsmodels.tsa.arima.model import ARIMA

def train_arima(series):

    model = ARIMA(series, order=(5,1,0))

    model_fit = model.fit()

    return model_fit


def predict_arima(model):

    forecast = model.forecast(steps=1)

    # Get first value safely
    return forecast.iloc[0]
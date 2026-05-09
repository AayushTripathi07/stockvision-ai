from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def evaluate_model(true, predicted):

    mae = mean_absolute_error(true, predicted)

    rmse = np.sqrt(mean_squared_error(true, predicted))

    return {
        "MAE": mae,
        "RMSE": rmse
    }
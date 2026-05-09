import numpy as np

def portfolio_return(weights, returns):

    return np.sum(returns.mean() * weights)


def portfolio_volatility(weights, cov):

    return np.sqrt(
        np.dot(weights.T, np.dot(cov, weights))
    )
from app.features.technical_indicators import add_technical_indicators


def prepare_features(df):

    df = add_technical_indicators(df)

    return df
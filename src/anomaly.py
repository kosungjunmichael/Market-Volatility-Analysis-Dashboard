import pandas as pd
from sklearn.ensemble import IsolationForest


def add_anomalies(
    df: pd.DataFrame,
    feature_cols=("return", "vol_20"),
    contamination: float = 0.02,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Use IsolationForest to detect anomaly days (e.g., abnormal volatility).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with feature columns, e.g. 'return', 'vol_20'.
    feature_cols : tuple of str
        Columns used for anomaly detection.
    contamination : float
        Fraction of points to treat as anomalies.
    random_state : int
        Random seed.

    Returns
    -------
    pd.DataFrame
        Copy of df with 'anomaly' column (-1 = anomaly, 1 = normal).
    """
    df = df.copy()
    features = df[list(feature_cols)].dropna()

    if len(features) < 20:
        df["anomaly"] = pd.NA
        return df

    iso = IsolationForest(contamination=contamination, random_state=random_state)
    labels = iso.fit_predict(features)

    df["anomaly"] = pd.NA
    df.loc[features.index, "anomaly"] = labels
    return df

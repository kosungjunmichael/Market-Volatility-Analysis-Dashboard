import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def add_clusters(
    df: pd.DataFrame,
    feature_cols=("vol_20", "vol_60"),
    n_clusters: int = 3,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Run K-Means clustering on selected feature columns and add a 'cluster' label.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with feature columns, e.g. 'vol_20', 'vol_60'.
    feature_cols : tuple of str
        Column names to use as clustering features.
    n_clusters : int
        Number of clusters (regimes) to find.
    random_state : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        Copy of df with 'cluster' column.
    """
    df = df.copy()
    features = df[list(feature_cols)].dropna()

    if len(features) < n_clusters:
        df["cluster"] = pd.NA
        return df

    scaler = StandardScaler()
    X = scaler.fit_transform(features)

    model = KMeans(n_clusters=n_clusters, n_init=10, random_state=random_state)
    clusters = model.fit_predict(X)

    df["cluster"] = pd.NA
    df.loc[features.index, "cluster"] = clusters
    return df

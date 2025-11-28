import numpy as np
import pandas as pd


def add_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add log returns column to a price DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with a 'Close' column.

    Returns
    -------
    pd.DataFrame
        Copy of df with an added 'return' column.
    """
    df = df.copy()
    df["return"] = np.log(df["Close"] / df["Close"].shift(1))
    return df


def add_rolling_vol(df: pd.DataFrame, windows=(20, 60, 120)) -> pd.DataFrame:
    """
    Add rolling annualized volatility columns to a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with a 'return' column.
    windows : tuple of int
        Rolling windows (in days) for volatility calculation.

    Returns
    -------
    pd.DataFrame
        Copy of df with columns 'vol_<window>'.
    """
    df = df.copy()
    for window in windows:
        col_name = f"vol_{window}"
        df[col_name] = df["return"].rolling(window).std() * np.sqrt(252)
    return df


def add_volume_features(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Add rolling average volume to a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'Volume' column.
    window : int
        Rolling window size for average volume.

    Returns
    -------
    pd.DataFrame
        Copy of df with 'vol_avg_<window>' column.
    """
    df = df.copy()
    df[f"vol_avg_{window}"] = df["Volume"].rolling(window).mean()
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convenience function to add all standard features:
    - log returns
    - 20/60/120d rolling volatility
    - 20d rolling average volume

    Parameters
    ----------
    df : pd.DataFrame
        Raw OHLCV DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with engineered features.
    """
    df = add_returns(df)
    df = add_rolling_vol(df, windows=(20, 60, 120))
    df = add_volume_features(df, window=20)
    return df

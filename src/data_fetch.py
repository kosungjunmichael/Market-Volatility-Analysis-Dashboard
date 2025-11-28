import yfinance as yf
import pandas as pd


def fetch_data_yfinance(ticker: str, period: str = "2y", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a given ticker using yfinance.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol, e.g. "AAPL".
    period : str
        Time period to download, e.g. "1y", "2y", "5y".
    interval : str
        Data interval, e.g. "1d", "1wk", "1mo".

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: Open, High, Low, Close, Volume.
    """
    data = yf.download(ticker, period=period, interval=interval, auto_adjust=True)

    if data.empty:
        raise ValueError(f"No price data returned for ticker '{ticker}'.")

    # Keep only needed columns
    data = data[["Open", "High", "Low", "Close", "Volume"]]
    return data

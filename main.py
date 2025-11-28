from src.data_fetch import fetch_data_yfinance
from src.features import add_features
from src.clustering import add_clusters
from src.anomaly import add_anomalies
from src.plotting import plot_dashboard


def main():
    print("=== Market Volatility Dashboard ===")
    ticker = input("Enter a stock ticker (e.g. AAPL, TSLA, MSFT): ").strip().upper()

    if not ticker:
        print("No ticker entered. Exiting.")
        return

    print(f"\nFetching data for {ticker}...")
    df = fetch_data_yfinance(ticker, period="2y", interval="1d")

    print("Adding features (returns, volatility, volume)...")
    df = add_features(df)

    print("Running K-Means clustering on volatility...")
    df = add_clusters(df, feature_cols=("vol_20", "vol_60"), n_clusters=3)

    print("Running anomaly detection (IsolationForest)...")
    df = add_anomalies(df, feature_cols=("return", "vol_20"), contamination=0.02)

    print("Generating volatility dashboard...")
    plot_dashboard(df, ticker)
    print("Done.")


if __name__ == "__main__":
    main()

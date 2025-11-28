import pandas as pd
import matplotlib.pyplot as plt


def plot_dashboard(df: pd.DataFrame, ticker: str):
    """
    Create a 3x2 volatility dashboard figure:
    1. Price + 20d vol
    2. 20/60/120d rolling vol
    3. Return histogram
    4. Vol_20 vs Volume (colored by cluster)
    5. Price by cluster regime
    6. 20d vol with anomaly markers
    """
    fig, axes = plt.subplots(3, 2, figsize=(16, 12))
    fig.suptitle(f"{ticker} – Market Volatility Dashboard", fontsize=16)

    # --- Chart 1: Price + 20d Volatility ---
    ax = axes[0, 0]
    ax.plot(df.index, df["Close"], label="Price")
    ax2 = ax.twinx()
    ax2.plot(df.index, df["vol_20"], linestyle="--", label="20d Volatility")
    ax.set_title("Price & 20d Volatility")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax2.set_ylabel("Volatility")

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    # --- Chart 2: Multi-window volatility ---
    ax = axes[0, 1]
    ax.plot(df.index, df["vol_20"], label="20d")
    ax.plot(df.index, df["vol_60"], label="60d")
    ax.plot(df.index, df["vol_120"], label="120d")
    ax.set_title("Rolling Volatility (20 / 60 / 120 days)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Annualized Volatility")
    ax.legend()

    # --- Chart 3: Return histogram ---
    ax = axes[1, 0]
    df["return"].dropna().hist(ax=ax, bins=50)
    ax.set_title("Daily Log Returns Distribution")
    ax.set_xlabel("Daily Log Return")
    ax.set_ylabel("Frequency")

    # --- Chart 4: Volatility vs Volume (clusters) ---
    ax = axes[1, 1]
    sub = df[["vol_20", "Volume", "cluster"]].dropna()
    if not sub.empty:
        scatter = ax.scatter(sub["vol_20"], sub["Volume"], c=sub["cluster"], cmap="viridis")
        ax.set_title("20d Volatility vs Volume (clusters)")
        ax.set_xlabel("20d Volatility")
        ax.set_ylabel("Volume")
        cbar = fig.colorbar(scatter, ax=ax)
        cbar.set_label("Cluster")
    else:
        ax.set_title("20d Volatility vs Volume (no cluster data)")
        ax.set_xlabel("20d Volatility")
        ax.set_ylabel("Volume")

    # --- Chart 5: Price by Volatility Regime ---
    ax = axes[2, 0]
    if "cluster" in df.columns and df["cluster"].notna().any():
        for c in sorted(df["cluster"].dropna().unique()):
            mask = df["cluster"] == c
            ax.plot(df.index[mask], df["Close"][mask], marker="o", linestyle="-", label=f"Cluster {c}")
        ax.legend()
    else:
        ax.plot(df.index, df["Close"])
    ax.set_title("Price by Volatility Regime")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")

    # --- Chart 6: 20d Volatility with anomalies ---
    ax = axes[2, 1]
    ax.plot(df.index, df["vol_20"], label="20d Volatility")
    if "anomaly" in df.columns and df["anomaly"].notna().any():
        anomalies = df[df["anomaly"] == -1]
        ax.scatter(anomalies.index, anomalies["vol_20"], s=40, label="Anomaly")
    ax.set_title("20d Volatility with Anomalies")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volatility")
    ax.legend()

    plt.subplots_adjust(
    left=0.07,
    right=0.97,
    top=0.92,
    bottom=0.06,
    hspace=0.40,
    wspace=0.30
    )   

    plt.show()


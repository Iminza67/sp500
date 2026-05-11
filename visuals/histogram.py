import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm


def create_returns_histogram(df: pd.DataFrame, symbol: str, bins: int = 50):
    """
    Production-ready returns histogram with normal distribution overlay.
    Uses precomputed 'DailyReturn' column from parquet dataset.
    """

    # -------------------------
    # SAFETY CHECKS
    # -------------------------
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_cols = {"Symbol", "DailyReturn"}

    if not required_cols.issubset(df.columns):
        raise ValueError(
            f"Missing required columns: {required_cols - set(df.columns)}"
        )

    # -------------------------
    # FILTER SYMBOL
    # -------------------------
    stock_df = df[df["Symbol"] == symbol].copy()

    if stock_df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")

    returns = stock_df["DailyReturn"].dropna()

    if len(returns) < 10:
        raise ValueError(f"Not enough return data for {symbol}")

    # -------------------------
    # STATS
    # -------------------------
    mean = returns.mean()
    std = returns.std()

    # avoid crash on flat data
    if std == 0 or np.isnan(std):
        std = 1e-6

    # -------------------------
    # HISTOGRAM (NORMALIZED)
    # -------------------------
    hist = go.Histogram(
        x=returns,
        nbinsx=bins,
        name="Returns",
        opacity=0.75,
        histnorm="probability density"
    )

    # -------------------------
    # NORMAL DISTRIBUTION CURVE
    # -------------------------
    x_vals = np.linspace(returns.min(), returns.max(), 200)
    y_vals = norm.pdf(x_vals, mean, std)

    normal_curve = go.Scatter(
        x=x_vals,
        y=y_vals,
        mode="lines",
        name="Normal Distribution",
        line=dict(width=2)
    )

    # -------------------------
    # MEAN & STD LINES
    # -------------------------
    mean_line = go.Scatter(
        x=[mean, mean],
        y=[0, max(y_vals)],
        mode="lines",
        name="Mean",
        line=dict(dash="dash")
    )

    std_plus = go.Scatter(
        x=[mean + std, mean + std],
        y=[0, max(y_vals)],
        mode="lines",
        name="+1 Std",
        line=dict(dash="dot")
    )

    std_minus = go.Scatter(
        x=[mean - std, mean - std],
        y=[0, max(y_vals)],
        mode="lines",
        name="-1 Std",
        line=dict(dash="dot")
    )

    # -------------------------
    # FIGURE
    # -------------------------
    fig = go.Figure(data=[
        hist,
        normal_curve,
        mean_line,
        std_plus,
        std_minus
    ])

    fig.update_layout(
        title=f"{symbol} Return Distribution",
        template="plotly_dark",
        height=500,
        xaxis_title="Daily Returns",
        yaxis_title="Density",
        bargap=0.1,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig
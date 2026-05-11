import pandas as pd
import plotly.graph_objects as go


def create_volatility_chart(df: pd.DataFrame, symbol: str):
    """
    Precomputed volatility visualization (production-ready).
    Uses dataset-level volatility from preprocessing stage.
    """

    # -------------------------
    # SAFETY CHECKS
    # -------------------------
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_cols = {"Symbol", "Date", "Volatility"}

    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing columns: {required_cols - set(df.columns)}")

    # -------------------------
    # FILTER SYMBOL
    # -------------------------
    stock_df = df[df["Symbol"] == symbol].copy()

    if stock_df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")

    # -------------------------
    # SORT
    # -------------------------
    stock_df = stock_df.sort_values("Date")

    # -------------------------
    # OPTIONAL SMOOTHING (VISUAL ONLY)
    # -------------------------
    stock_df["Volatility_MA30"] = stock_df["Volatility"].rolling(30).mean()

    # -------------------------
    # FIGURE
    # -------------------------
    fig = go.Figure()

    # raw volatility
    fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["Volatility"],
            mode="lines",
            name="Daily Volatility",
            line=dict(width=1)
        )
    )

    # smoothed volatility
    fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["Volatility_MA30"],
            mode="lines",
            name="30-Day MA",
            line=dict(width=3)
        )
    )

    # -------------------------
    # BENCHMARK LINE
    # -------------------------
    mean_vol = stock_df["Volatility"].mean()

    fig.add_hline(
        y=mean_vol,
        line_dash="dash",
        line_color="gray",
        annotation_text="Avg Volatility"
    )

    # -------------------------
    # STYLE
    # -------------------------
    fig.update_layout(
        title=f"{symbol} Volatility Over Time",
        template="plotly_dark",
        height=500,
        xaxis_title="Date",
        yaxis_title="Volatility",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig
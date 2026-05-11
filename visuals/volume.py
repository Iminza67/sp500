import pandas as pd
import plotly.graph_objects as go


def create_volume_chart(df: pd.DataFrame, symbol: str):
    """
    Production-ready volume chart.
    Uses preprocessed OHLCV data from parquet.
    """

    # -------------------------
    # SAFETY CHECKS
    # -------------------------
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_cols = {"Symbol", "Date", "Volume"}

    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing columns: {required_cols - set(df.columns)}")

    # -------------------------
    # FILTER SYMBOL
    # -------------------------
    stock_df = df[df["Symbol"] == symbol].copy()

    if stock_df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")

    # -------------------------
    # CLEAN + SORT
    # -------------------------
    stock_df = stock_df.sort_values("Date")

    # ensure numeric safety
    stock_df["Volume"] = pd.to_numeric(stock_df["Volume"], errors="coerce")
    stock_df = stock_df.dropna(subset=["Volume"])

    # remove invalid values
    stock_df = stock_df[stock_df["Volume"] > 0]

    # -------------------------
    # OPTIONAL: SMOOTHING (VISUAL ONLY)
    # -------------------------
    stock_df["Volume_MA20"] = stock_df["Volume"].rolling(20).mean()

    # -------------------------
    # FIGURE
    # -------------------------
    fig = go.Figure()

    # raw volume
    fig.add_trace(
        go.Bar(
            x=stock_df["Date"],
            y=stock_df["Volume"],
            name="Volume",
            marker_color="steelblue"
        )
    )

    # moving average (helps readability for finance charts)
    fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["Volume_MA20"],
            mode="lines",
            name="20-Day MA",
            line=dict(width=2, color="orange")
        )
    )

    # -------------------------
    # AVERAGE LINE
    # -------------------------
    avg_volume = stock_df["Volume"].mean()

    fig.add_hline(
        y=avg_volume,
        line_dash="dash",
        line_color="red",
        annotation_text="Avg Volume"
    )

    # -------------------------
    # STYLE
    # -------------------------
    fig.update_layout(
        title=f"{symbol} Trading Volume",
        template="plotly_dark",
        height=450,
        xaxis_title="Date",
        yaxis_title="Volume",
        yaxis=dict(rangemode="tozero"),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig
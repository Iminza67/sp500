import pandas as pd
import plotly.graph_objects as go


def create_candlestick_chart(df: pd.DataFrame, symbol: str, ma_window: int = 20):
    """
    Production-ready candlestick chart generator.
    Assumes pre-cleaned dataset from parquet pipeline.
    """

    # -------------------------
    # SAFETY CHECKS
    # -------------------------
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_cols = {"Date", "Symbol", "Open", "High", "Low", "Close"}

    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing required columns: {required_cols - set(df.columns)}")

    # -------------------------
    # FILTER SYMBOL (FAST)
    # -------------------------
    stock_df = df.loc[df["Symbol"] == symbol].copy()

    if stock_df.empty:
        raise ValueError(f"No data found for symbol: {symbol}")

    # -------------------------
    # CLEAN + SORT
    # -------------------------
    stock_df = stock_df.sort_values("Date")

    # ensure numeric safety (important for plotting stability)
    stock_df[["Open", "High", "Low", "Close"]] = stock_df[
        ["Open", "High", "Low", "Close"]
    ].apply(pd.to_numeric, errors="coerce")

    stock_df = stock_df.dropna(subset=["Open", "High", "Low", "Close"])

    # -------------------------
    # CREATE FIGURE
    # -------------------------
    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=stock_df["Date"],
            open=stock_df["Open"],
            high=stock_df["High"],
            low=stock_df["Low"],
            close=stock_df["Close"],
            name=symbol
        )
    )

    # -------------------------
    # MOVING AVERAGE (OPTIONAL)
    # -------------------------
    if ma_window and ma_window > 0:
        stock_df["MA"] = stock_df["Close"].rolling(ma_window).mean()

        fig.add_trace(
            go.Scatter(
                x=stock_df["Date"],
                y=stock_df["MA"],
                mode="lines",
                name=f"{ma_window}-Day MA",
                line=dict(width=2)
            )
        )

    # -------------------------
    # LAYOUT (CLEAN UI)
    # -------------------------
    fig.update_layout(
        title=f"{symbol} Candlestick Chart",
        template="plotly_dark",   # better for dashboards
        height=500,
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h")
    )

    return fig
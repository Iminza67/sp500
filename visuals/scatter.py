import plotly.express as px
import pandas as pd


def create_scatter_plot(df: pd.DataFrame):
    """
    Risk vs Return scatter plot (production-ready).
    Uses precomputed DailyReturn from parquet dataset.
    """

    # -------------------------
    # SAFETY CHECKS
    # -------------------------
    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty.")

    required_cols = {"Symbol", "DailyReturn", "Volatility", "Marketcap", "Sector"}

    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing columns: {required_cols - set(df.columns)}")

    # -------------------------
    # AGGREGATE PER SYMBOL
    # -------------------------
    agg_df = df.groupby("Symbol").agg(
        mean_return=("DailyReturn", "mean"),
        volatility=("Volatility", "std"),
        marketcap=("Marketcap", "first"),
        sector=("Sector", "first")
    ).reset_index()

    # -------------------------
    # CLEAN
    # -------------------------
    agg_df = agg_df.dropna(subset=["mean_return", "volatility"])

    # -------------------------
    # OPTIONAL: ANNUALIZATION (CLEAR + LABELED)
    # -------------------------
    agg_df["mean_return"] = agg_df["mean_return"] * 252 * 100
    agg_df["volatility"] = agg_df["volatility"] * (252 ** 0.5) * 100

    # -------------------------
    # SCATTER PLOT
    # -------------------------
    fig = px.scatter(
        agg_df,
        x="volatility",
        y="mean_return",
        size="marketcap",
        color="sector",
        hover_name="Symbol",
        hover_data={
            "mean_return": ":.2f",
            "volatility": ":.2f",
            "sector": True,
            "marketcap": True
        },
        title="Risk vs Return (Annualized)",
        size_max=45
    )

    # -------------------------
    # BENCHMARK LINES
    # -------------------------
    fig.add_hline(
        y=agg_df["mean_return"].mean(),
        line_dash="dash",
        line_color="gray"
    )

    fig.add_vline(
        x=agg_df["volatility"].mean(),
        line_dash="dash",
        line_color="gray"
    )

    # -------------------------
    # STYLE
    # -------------------------
    fig.update_traces(
        marker=dict(
            opacity=0.75,
            line=dict(width=0.5, color="black")
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=650,
        xaxis_title="Volatility (%)",
        yaxis_title="Return (%)",
        legend_title="Sector",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig
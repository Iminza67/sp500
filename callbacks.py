from app import app
from dash import Input, Output
from data.data_loader import load_data

from visuals.candlestick import create_candlestick_chart
from visuals.volatility import create_volatility_chart
from visuals.volume import create_volume_chart
from visuals.scatter import create_scatter_plot
from visuals.histogram import create_returns_histogram


# -------------------------
# LOAD DATA ONCE
# -------------------------
df = load_data()


# =========================
# SAFE WRAPPER (IMPORTANT)
# =========================
def safe_call(func, *args):
    try:
        return func(*args)
    except Exception as e:
        print(f"❌ Error in {func.__name__}: {e}")

        # fallback visible figure so dashboard doesn't go blank
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.update_layout(title=f"Error in {func.__name__}: check console")
        return fig


# =========================
# CANDLESTICK
# =========================
@app.callback(
    Output("candlestick", "figure"),
    Input("symbol", "value")
)
def update_candlestick(symbol):
    print("CALLBACK FIRED:",symbol)
    return safe_call(create_candlestick_chart, df, symbol)


# =========================
# VOLATILITY
# =========================
@app.callback(
    Output("volatility", "figure"),
    Input("symbol", "value")
)
def update_volatility(symbol):
    return safe_call(create_volatility_chart, df, symbol)


# =========================
# VOLUME
# =========================
@app.callback(
    Output("volume", "figure"),
    Input("symbol", "value")
)
def update_volume(symbol):
    return safe_call(create_volume_chart, df, symbol)


# =========================
# SCATTER
# =========================
@app.callback(
    Output("scatter", "figure"),
    Input("symbol", "value")
)
def update_scatter(symbol):
    return safe_call(create_scatter_plot, df)


# =========================
# HISTOGRAM
# =========================
@app.callback(
    Output("histogram", "figure"),
    Input("symbol", "value")
)
def update_histogram(symbol):
    return safe_call(create_returns_histogram, df, symbol)
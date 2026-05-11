from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

from data.data_loader import load_data

from visuals.candlestick import create_candlestick_chart
from visuals.volatility import create_volatility_chart
from visuals.volume import create_volume_chart
from visuals.scatter import create_scatter_plot
from visuals.histogram import create_returns_histogram


# -------------------------
# LOAD DATA (safe for Azure)
# -------------------------
df = load_data()
symbols = sorted(df["Symbol"].unique())


# -------------------------
# INIT APP
# -------------------------
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True
)

server = app.server   # 🔥 REQUIRED for Azure / Gunicorn


# -------------------------
# LAYOUT
# -------------------------
app.layout = dbc.Container([

    html.H1("📊 S&P 500 Analytics Dashboard", className="text-center mt-3"),
    html.Hr(),

    # Dropdown
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="symbol",
                options=[{"label": s, "value": s} for s in symbols],
                value=symbols[0] if symbols else None,
                clearable=False
            )
        ], width=4)
    ]),

    html.Br(),

    # Charts
    dbc.Row([
        dbc.Col(dcc.Graph(id="candlestick"), width=6),
        dbc.Col(dcc.Graph(id="volatility"), width=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id="volume"), width=6),
        dbc.Col(dcc.Graph(id="scatter"), width=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id="histogram"), width=12),
    ])

], fluid=True)


# -------------------------
# CALLBACKS
# -------------------------
@app.callback(
    Output("candlestick", "figure"),
    Input("symbol", "value")
)
def update_candlestick(symbol):
    return create_candlestick_chart(df, symbol)


@app.callback(
    Output("volatility", "figure"),
    Input("symbol", "value")
)
def update_volatility(symbol):
    return create_volatility_chart(df, symbol)


@app.callback(
    Output("volume", "figure"),
    Input("symbol", "value")
)
def update_volume(symbol):
    return create_volume_chart(df, symbol)


@app.callback(
    Output("scatter", "figure"),
    Input("symbol", "value")
)
def update_scatter(symbol):
    return create_scatter_plot(df)


@app.callback(
    Output("histogram", "figure"),
    Input("symbol", "value")
)
def update_histogram(symbol):
    return create_returns_histogram(df, symbol)


# -------------------------
# LOCAL RUN ONLY (NOT USED IN AZURE)
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
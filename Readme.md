# S&P 500 Analytics Dashboard

An interactive financial analytics dashboard built with Python, Dash, Plotly, and Pandas for analyzing S&P 500 stock market data.

---

## 🚀 Live Dashboard

Here is the live dashboard:

```text
https://sp500-dzxz.onrender.com/
```

---

# 📊 Project Overview

This project provides an interactive analytics platform for exploring historical S&P 500 stock data through advanced visualizations and financial metrics.

The dashboard allows users to:

* Analyze stock price movements
* Explore trading volume patterns
* Measure market volatility
* Visualize return distributions
* Compare risk vs return relationships
* Interact with financial charts dynamically

---

# 📈 Dashboard Features

## 📉 Candlestick Charts

Interactive OHLC candlestick charts for stock price analysis.

## 📊 Volume Analysis

Visualize historical trading volume trends and liquidity.

## ⚡ Volatility Tracking

Rolling volatility calculations for risk analysis.

## 📌 Return Distribution Histogram

Distribution analysis of stock returns.

## 📍 Risk vs Return Scatter Plot

Compares annualized return against volatility across companies.

## 🔍 Interactive Filtering

Dynamic stock selection using dropdown components.

---

# 🛠️ Technologies Used

## Backend

* Python
* Pandas
* NumPy
* SciPy

## Dashboard & Visualization

* Dash
* Plotly
* Dash Bootstrap Components

## Data Storage & Optimization

* Parquet
* PyArrow

## Deployment

* Azure Web App
* Gunicorn

---

# 📁 Project Structure

```text
sp500/
│
├── app.py
├── requirements.txt
├── preprocess.py
│
├── data/
│   ├── financials.csv
│   ├── sp500_companies.csv
│   ├── sp500_stocks.csv
│   ├── sp500_analysis_ready.parquet
│   └── data_loader.py
│
├── visuals/
│   ├── candlestick.py
│   ├── histogram.py
│   ├── scatter.py
│   ├── volatility.py
│   ├── volume.py
│   └── heatmap.py
│
└── assets/
```

---

# ⚙️ Data Preprocessing Pipeline

The preprocessing pipeline was designed to optimize dashboard performance and cloud deployment.

## Pipeline Tasks

* Clean missing OHLCV data
* Filter valid stocks with sufficient historical records
* Merge company metadata with stock data
* Generate derived financial metrics
* Compute daily returns
* Compute rolling volatility
* Log-transform trading volume
* Export optimized Parquet datasets

---

# 📊 Financial Metrics Included

* Daily Returns
* Rolling Volatility
* Trading Volume
* Market Capitalization
* Sector Classification
* Industry Classification
* Price Statistics

---

# 🚀 Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd sp500
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Dashboard Locally

Run preprocessing:

```bash
python preprocess.py
```

Start the dashboard:

```bash
python app.py
```

Dashboard runs locally at:

```text
http://127.0.0.1:8050/
```

---

# ☁️ Azure Deployment

The dashboard is configured for Azure Web App deployment.

## Production Startup Command

```bash
gunicorn app:server
```

---

# 📊 Performance Optimization

To improve deployment performance and reduce memory usage:

* Parquet format was used instead of CSV
* Large datasets were preprocessed before deployment
* Financial metrics were precomputed
* Dataset filtering reduced unnecessary processing
* Visualizations use optimized subsets of data

---

# 🔍 Future Improvements

* Real-time stock market streaming
* Portfolio optimization tools
* Sector performance heatmaps
* Correlation analysis
* Technical indicators
* Machine learning forecasting
* User authentication
* Cloud caching layer

---

# 📚 Learning Outcomes

This project demonstrates:

* Financial data engineering
* Time series analysis
* Interactive dashboard development
* Data preprocessing pipelines
* Cloud deployment workflows
* Financial visualization techniques
* Performance optimization for large datasets

---

# 👩‍💻 Author

Olivia Iminza Hamisi
Bachelor of Science in Engineering (Informatics)
IMC University of Applied Sciences Krems

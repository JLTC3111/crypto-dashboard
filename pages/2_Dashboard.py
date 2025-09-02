import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from helpers.pricing import get_price_history, get_current_prices
from helpers.risk import max_drawdown, sharpe_ratio, value_at_risk
from helpers.export import export_pdf
from helpers.crypto_config import get_sorted_crypto_list, get_symbol_from_name, get_symbol_map

# Set wide layout for better display
st.set_page_config(page_title="Crypto Risk Dashboard", page_icon="🛝", layout="wide")

st.title("📊 Crypto Risk Management Dashboard")

# Use comprehensive top 200 crypto list
symbol_map = get_symbol_map()
crypto_list = get_sorted_crypto_list()

selection = st.selectbox("Choose an asset:", crypto_list)
symbol = symbol_map[selection]

# Fetch historical data and capture status
with st.spinner(f"Fetching data for {selection}..."):
    # Redirect stdout to capture API status messages
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        history = get_price_history(symbol)
        output_text = captured_output.getvalue()
    finally:
        sys.stdout = old_stdout

# Check if data was successfully fetched
if history is None or history.empty:
    st.error("❌ **No Data Available**: Unable to fetch price data from any API. Please check your internet connection or try again later.")
    st.stop()

# Show data source status
if "CoinGecko data fetched" in output_text:
    st.success("🦎 **Live Data**: Using real-time data from CoinGecko API")
elif "Coinbase" in output_text:
    st.info("💰 **Alternative Data**: Using Coinbase API fallback")
elif "Created minimal data" in output_text:
    st.warning("📊 **Backup Data**: Using synthetic data (APIs temporarily unavailable)")
else:
    st.info("📊 **Data Source**: Cryptocurrency price data")

# Use 'close' prices
price_series = history["close"]

# Use 'close' prices

# Check data source and provide user feedback
has_binance_api = False
try:
    has_binance_api = bool(st.secrets.get("binance_api", {}).get("api_key", ""))
except:
    pass

if has_binance_api:
    st.success("🔑 **Live Data**: Using real-time data from authenticated Binance API")
else:
    st.info("� **Public Data**: Using public Binance API (no authentication required for price data)")

# Show warning if no data is fetched
if history is None or history.empty:
    st.error("❌ **No Data Available**: Unable to fetch price data from Binance API. Please check your internet connection or try again later.")
    st.stop()

if history is None or history.empty:
    st.error("No historical data available.")
    st.stop()

# Use 'close' prices
price_series = history["close"]
timestamps = history.index
latest_price = float(price_series.iloc[-1])

# Metrics
md = float(max_drawdown(price_series))
sr = float(sharpe_ratio(price_series))
var = float(value_at_risk(price_series))

# --- Risk Indicator ---
def risk_indicator(sharpe_ratio):
    if sharpe_ratio > 2:
        return "✅ Low Risk"
    elif sharpe_ratio > 1:
        return "⚠️ Medium Risk"
    else:
        return "🚨 High Risk"

# --- Alert Thresholds ---
st.sidebar.header("Technical Analysis")
sma_options = st.sidebar.multiselect(
    "Simple Moving Averages (SMAs)",
    [20, 50, 100, 200],
    default=[20, 50]
)

st.sidebar.header("Economic Factors")
st.sidebar.text_area("Notes on macro events, news, etc.", key='eco_notes')

st.sidebar.header("Alerts")
high_alert = st.sidebar.number_input("High (Sell) Alert", value=0.0, step=0.01, key='high_alert')
low_alert = st.sidebar.number_input("Low (Buy) Alert", value=0.0, step=0.01, key='low_alert')

if high_alert > 0 and latest_price > high_alert:
    st.error(f"🚨 SELL ALERT: {selection} has passed your high threshold of ${high_alert:,.2f}!")

if low_alert > 0 and latest_price < low_alert:
    st.success(f"✅ BUY ALERT: {selection} has dropped below your low threshold of ${low_alert:,.2f}!")


# --- Display Metrics ---
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("💰 Current Price (USD)", f"${latest_price:,.2f}")
with col2:
    st.metric("📉 Max Drawdown", f"{md:.2%}")
with col3:
    st.metric("⚖️ Sharpe Ratio", f"{sr:.2f}")
with col4:
    st.metric("📊 VaR (95%)", f"{var:.2%}")
with col5:
    st.metric("Risk Level", risk_indicator(sr))

# --- Performance Ratios ---
st.subheader("Performance Ratios")
r_col1, r_col2 = st.columns(2)

# Get current prices for ratio calculations
if symbol not in ['BTC', 'ETH']:
    try:
        # Get current prices for ratios
        ratio_symbols = []
        if symbol != 'BTC':
            ratio_symbols.append('BTC')
        if symbol != 'ETH':
            ratio_symbols.append('ETH')
        
        if ratio_symbols:
            ratio_symbols.append(symbol)
            current_prices = get_current_prices(ratio_symbols)
            
            if symbol != 'BTC' and current_prices.get('BTC', 0) > 0 and current_prices.get(symbol, 0) > 0:
                btc_ratio = current_prices[symbol] / current_prices['BTC']
                r_col1.metric(f"{symbol}/BTC", f"{btc_ratio:.8f}")
            
            if symbol != 'ETH' and current_prices.get('ETH', 0) > 0 and current_prices.get(symbol, 0) > 0:
                eth_ratio = current_prices[symbol] / current_prices['ETH']
                r_col2.metric(f"{symbol}/ETH", f"{eth_ratio:.8f}")
    except Exception as e:
        r_col1.info("Ratio data temporarily unavailable")
        r_col2.info("Ratio data temporarily unavailable")


# --- Price Chart ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=timestamps, y=price_series, mode='lines', name=symbol, line=dict(color='blue')))

# Add SMAs to chart
for sma in sma_options:
    sma_series = price_series.rolling(window=sma).mean()
    fig.add_trace(go.Scatter(x=timestamps, y=sma_series, mode='lines', name=f'{sma}-Day SMA'))

fig.update_layout(title=f"{selection} - Price History with SMAs", xaxis_title="", yaxis_title="Price (USD)")
st.plotly_chart(fig, use_container_width=True)

# --- Export CSV ---
csv = history.to_csv(index=True)
st.download_button("Download CSV", csv, file_name=f"{symbol}_history.csv", mime='text/csv')

# --- Export PDF ---
pdf_metrics = {
    "Current Price": f"${latest_price:,.2f}",
    "Max Drawdown": f"{md:.2%}",
    "Sharpe Ratio": f"{sr:.2f}",
    "VaR (95%)": f"{var:.2%}"
}
st.download_button(
    label="Download PDF Report",
    data=export_pdf(pdf_metrics),
    file_name="risk_report.pdf",
    mime="application/pdf"
)

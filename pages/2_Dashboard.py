import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from helpers.modern_ui import (
    ModernUI, 
    create_modern_sidebar,
    create_modern_header,
    create_glass_card,
    create_modern_metric_card
)
from helpers.i18n import t
from helpers.svg_icons import get_svg_icon
from helpers.pricing import get_price_history, get_current_prices
from helpers.risk import max_drawdown, sharpe_ratio, value_at_risk
from helpers.export import export_pdf
from helpers.crypto_config import get_sorted_crypto_list, get_symbol_from_name, get_symbol_map

# Page Configuration
st.set_page_config(
    page_title="Crypto Risk Dashboard",
    page_icon="📊",
    layout="wide"
)

# Apply modern theme
ModernUI.apply_modern_theme()

# Create modern sidebar
create_modern_sidebar()

# Modern header
create_modern_header(
    "Asset Risk Dashboard",
    "Analyze cryptocurrency risk profiles with advanced metrics and visualizations",
    icon="chart"
)

# Use comprehensive top 200 crypto list
symbol_map = get_symbol_map()
crypto_list = get_sorted_crypto_list()

# Asset selection in a modern card
asset_selection_html = f"""
<div class="glass-card" style="margin-bottom: 1.5rem;">
    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
        {get_svg_icon('settings', size=20)}
        <h3 style="margin: 0; font-weight: 600;">Configuration</h3>
    </div>
</div>
"""
st.markdown(asset_selection_html, unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    from helpers.crypto_config import CRYPTO_ASSETS
    
    # Extract symbols and names
    asset_options = {f"{coin['symbol']} - {coin['name']}": coin['symbol'] 
                    for coin in CRYPTO_ASSETS}
    
    # Asset selection
    selection = st.selectbox(
        "🪙 Select Cryptocurrency",
        options=list(asset_options.keys()),
        index=0
    )
    
    selected_symbol = asset_options[selection]

with col2:
    # Time period selection
    period_options = {
        "1 Week": 7,
        "1 Month": 30,
        "3 Months": 90,
        "6 Months": 180,
        "1 Year": 365,
        "3 Years": 1095,
        "5 Years": 1825
    }
    
    period_label = st.selectbox(
        "📅 Time Period",
        options=list(period_options.keys()),
        index=4  # Default to 1 Year
    )
    
    days = period_options[period_label]

# Fetch historical data and capture status
with st.spinner(f"Fetching data for {selection}..."):
    # Redirect stdout to capture API status messages
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        history = get_price_history(selected_symbol, days=days)
        output_text = captured_output.getvalue()
    finally:
        sys.stdout = old_stdout

# Determine data source from captured output
data_source = "Unknown"
if "Binance data fetched" in output_text:
    data_source = "Binance API"
elif "CoinGecko data fetched" in output_text:
    data_source = "CoinGecko API"
elif "Created minimal data" in output_text:
    data_source = "Fallback Data"

# Check if data was successfully fetched
if history is None or history.empty:
    st.error("❌ **No Data Available**: Unable to fetch price data from any API. Please check your internet connection or try again later.")
    st.stop()

# Show data source status
if data_source == "Binance API":
    st.success(f"🔑 **Live Data**: Using real-time data from {data_source}")
elif data_source == "CoinGecko API":
    st.info(f"🦎 **Alternative Data**: Using data from {data_source} (Binance unavailable)")
else:
    st.warning(f"📊 **Backup Data**: Using {data_source} (APIs temporarily unavailable)")

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
if selected_symbol not in ['BTC', 'ETH']:
    try:
        # Get current prices for ratios
        ratio_symbols = []
        if selected_symbol != 'BTC':
            ratio_symbols.append('BTC')
        if selected_symbol != 'ETH':
            ratio_symbols.append('ETH')
        
        if ratio_symbols:
            ratio_symbols.append(selected_symbol)
            current_prices = get_current_prices(ratio_symbols)
            
            if selected_symbol != 'BTC' and current_prices.get('BTC', 0) > 0 and current_prices.get(selected_symbol, 0) > 0:
                btc_ratio = current_prices[selected_symbol] / current_prices['BTC']
                r_col1.metric(f"{selected_symbol}/BTC", f"{btc_ratio:.8f}")
            
            if selected_symbol != 'ETH' and current_prices.get('ETH', 0) > 0 and current_prices.get(selected_symbol, 0) > 0:
                eth_ratio = current_prices[selected_symbol] / current_prices['ETH']
                r_col2.metric(f"{selected_symbol}/ETH", f"{eth_ratio:.8f}")
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

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from helpers.pricing import get_price_history
from helpers.risk import max_drawdown, sharpe_ratio, value_at_risk
from helpers.crypto_config import get_sorted_crypto_list, get_symbol_from_name, get_symbol_map

# Set wide layout for better display
st.set_page_config(page_title="Asset Comparison", page_icon="⚖️", layout="wide")

st.title("⚖️ Asset Comparison")

# Use comprehensive top 200 crypto list
symbol_map = get_symbol_map()
crypto_list = get_sorted_crypto_list()

col1, col2 = st.columns(2)

with col1:
    selection1 = st.selectbox("Choose asset 1:", crypto_list, key='asset1')
    symbol1 = symbol_map[selection1]

with col2:
    available_assets_2 = [asset for asset in crypto_list if asset != selection1]
    selection2 = st.selectbox("Choose asset 2:", available_assets_2, key='asset2')
    symbol2 = symbol_map[selection2]

# Fetch historical data
with st.spinner(f"Fetching data for {selection1} and {selection2}..."):
    history1 = get_price_history(symbol1)
    history2 = get_price_history(symbol2)

# Check if we're using real API or mock data
import os
is_cloud = any([
    os.getenv('STREAMLIT_SHARING_MODE'),
    os.getenv('STREAMLIT_CLOUD'),
    'streamlit.app' in os.getenv('HOSTNAME', ''),
    '/app' in os.getcwd(),
    '/mount/src' in os.getcwd()  # New Streamlit Cloud path
])

# Check if we have Binance API credentials
has_binance_api = False
try:
    has_binance_api = bool(st.secrets.get("binance_api", {}).get("api_key", ""))
except:
    pass

if has_binance_api and not is_cloud:
    st.success("🔑 **Authenticated Local**: Using real-time data from authenticated Binance API")
elif has_binance_api and is_cloud:
    st.info("🔑 **Authenticated Cloud**: Using real-time data from authenticated Binance API on Streamlit Cloud")
elif not is_cloud:
    st.info("� **Public API**: Using public Binance API data")
else:
    st.warning("⚠️ **Demo Mode**: Using simulated data. Add Binance API credentials to Streamlit Cloud secrets for real data.")

# Check data availability and provide specific error messages
data1_available = history1 is not None and not history1.empty
data2_available = history2 is not None and not history2.empty

if not data1_available and not data2_available:
    st.error(f"❌ No historical data available for {selection1} and {selection2}. Please try different assets.")
    st.info("💡 Tip: Some assets like USDT or staked tokens may not have trading pairs on Binance.")
    st.stop()
elif not data1_available:
    st.error(f"❌ No historical data available for {selection1}. Please select a different asset.")
    st.info(f"Available data for {selection2}: {len(history2)} days")
    st.stop()
elif not data2_available:
    st.error(f"❌ No historical data available for {selection2}. Please select a different asset.")
    st.info(f"Available data for {selection1}: {len(history1)} days")
    st.stop()

# Show data availability info
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.success(f"✅ {selection1}: {len(history1)} days of data")
with col_info2:
    st.success(f"✅ {selection2}: {len(history2)} days of data")

# --- Metrics Comparison ---
price1 = history1['close']
price2 = history2['close']

metrics1 = {
    "Max Drawdown": max_drawdown(price1),
    "Sharpe Ratio": sharpe_ratio(price1),
    "Value at Risk (95%)": value_at_risk(price1)
}

metrics2 = {
    "Max Drawdown": max_drawdown(price2),
    "Sharpe Ratio": sharpe_ratio(price2),
    "Value at Risk (95%)": value_at_risk(price2)
}

st.subheader("Risk Metrics Comparison")

m_col1, m_col2 = st.columns(2)

with m_col1:
    st.write(f"**{selection1}**")
    st.metric("📉 Max Drawdown", f"{metrics1['Max Drawdown']:.2%}")
    st.metric("⚖️ Sharpe Ratio", f"{metrics1['Sharpe Ratio']:.2f}")
    st.metric("📊 VaR (95%)", f"{metrics1['Value at Risk (95%)']:.2%}")

with m_col2:
    st.write(f"**{selection2}**")
    st.metric("📉 Max Drawdown", f"{metrics2['Max Drawdown']:.2%}")
    st.metric("⚖️ Sharpe Ratio", f"{metrics2['Sharpe Ratio']:.2f}")
    st.metric("📊 VaR (95%)", f"{metrics2['Value at Risk (95%)']:.2%}")


# --- Correlation Analysis ---
returns1 = price1.pct_change().dropna()
returns2 = price2.pct_change().dropna()

# Align returns data
returns_df = pd.concat([returns1, returns2], axis=1, join='inner')
returns_df.columns = [selection1, selection2]

correlation = returns_df[selection1].corr(returns_df[selection2])

st.subheader("Correlation Analysis")
st.metric("Correlation Coefficient", f"{correlation:.2f}")

# --- Returns Scatter Plot ---
scatter_fig = go.Figure()
scatter_fig.add_trace(
    go.Scatter(
        x=returns_df[selection1],
        y=returns_df[selection2],
        mode='markers',
        marker=dict(size=5, opacity=0.6)
    )
)
scatter_fig.update_layout(
    title=f"Daily Returns: {selection1} vs. {selection2}",
    xaxis_title=f"{selection1} Returns",
    yaxis_title=f"{selection2} Returns"
)
st.plotly_chart(scatter_fig, use_container_width=True)


# --- Price Chart ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=history1.index, y=history1['close'], mode='lines', name=selection1))
fig.add_trace(go.Scatter(x=history2.index, y=history2['close'], mode='lines', name=selection2))
fig.update_layout(title="Price Comparison", xaxis_title="Date", yaxis_title="Price (USD)")
st.plotly_chart(fig, use_container_width=True)

# --- Analysis & Predictions ---
st.subheader("Analysis & Predictions")
st.text_area("Your notes on the comparison, best case scenarios, etc.", key='analysis_notes')

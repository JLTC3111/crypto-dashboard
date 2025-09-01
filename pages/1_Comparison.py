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

if history1 is None or history1.empty or history2 is None or history2.empty:
    st.error("No historical data available for one or both assets.")
    st.stop()

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

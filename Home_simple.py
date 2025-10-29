import streamlit as st

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Crypto Risk Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
from pycoingecko import CoinGeckoAPI
import time
from datetime import datetime

# Initialize CoinGecko API client
cg = CoinGeckoAPI()

# Basic UI without modern components
st.title("📊 Crypto Risk Dashboard")
st.markdown("Professional cryptocurrency risk management and analytics platform")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.info("Theme and language settings are temporarily disabled")

# Live Market Data Section
st.subheader("Live Market Data")

# Controls
col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
with col1:
    height_slider = st.slider(
        "📏 Table Height", 
        min_value=200, 
        max_value=1000, 
        value=500, 
        step=50,
        help="Adjust the height of the market data table"
    )
with col2:
    num_coins = st.selectbox(
        "🪙 Number of Coins", 
        [50, 100, 200, 300, 500], 
        index=1,
        help="Select how many cryptocurrencies to display"
    )
with col3:
    auto_refresh = st.checkbox(
        "🔄 Auto-refresh (20 min)", 
        value=False,
        help="Automatically refresh data every 20 minutes"
    )
with col4:
    if st.button(
        "↻ Refresh", 
        type="primary", 
        use_container_width=True,
        help="Manually refresh market data"
    ):
        st.cache_data.clear()
        st.rerun()

# Display last update time
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

st.caption(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

# Fetch and display data
@st.cache_data(ttl=1200)
def fetch_market_data(num_coins):
    """Fetch market data from CoinGecko with fallback"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            markets = cg.get_coins_markets(
                vs_currency='usd',
                order='market_cap_desc',
                per_page=num_coins,
                page=1,
                sparkline=False,
                price_change_percentage='7d'
            )
            
            df = pd.DataFrame(markets)
            
            # Select and rename columns
            columns_to_keep = {
                'market_cap_rank': 'Rank',
                'name': 'Name',
                'symbol': 'Symbol',
                'current_price': 'Price (USD)',
                'market_cap': 'Market Cap (USD)',
                'price_change_percentage_24h': '24h Change (%)',
                'price_change_percentage_7d_in_currency': '7d Change (%)',
                'circulating_supply': 'Circulating Supply',
                'total_supply': 'Total Supply',
                'max_supply': 'Max Supply',
                'ath': 'ATH (USD)',
                'ath_change_percentage': 'ATH Drawdown (%)'
            }
            
            df = df[list(columns_to_keep.keys())].rename(columns=columns_to_keep)
            
            return df
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:  # Rate limit error
                wait_time = 2 ** attempt  # Exponential backoff
                st.warning(f"Rate limited, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            st.error(f"Failed to fetch data from CoinGecko: {e}")
            return pd.DataFrame()

with st.spinner("Fetching live market data from CoinGecko..."):
    df = fetch_market_data(num_coins)
    
    if not df.empty:
        # Format the dataframe for display
        df['Symbol'] = df['Symbol'].str.upper()
        
        # Format numeric columns
        df['Price (USD)'] = df['Price (USD)'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "N/A")
        df['Market Cap (USD)'] = df['Market Cap (USD)'].apply(lambda x: f"${x:,.0f}" if pd.notnull(x) else "N/A")
        df['24h Change (%)'] = df['24h Change (%)'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A")
        df['7d Change (%)'] = df['7d Change (%)'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A")
        df['ATH (USD)'] = df['ATH (USD)'].apply(lambda x: f"${x:,.2f}" if pd.notnull(x) else "N/A")
        df['ATH Drawdown (%)'] = df['ATH Drawdown (%)'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A")
        
        # Display the dataframe
        st.dataframe(df, use_container_width=True, height=height_slider)
        
        # Display summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Coins Displayed", num_coins)
        with col2:
            st.metric("Data Provider", "CoinGecko API")
        with col3:
            st.metric("Update Frequency", "20 minutes (cached)")
        
        # Auto-refresh logic
        if auto_refresh:
            time.sleep(1200)  # 20 minutes
            st.session_state.last_update = datetime.now()
            st.rerun()
    else:
        st.error("Unable to fetch market data. Please check your internet connection or try again later.")

# Footer
st.markdown("---")
st.caption("Data provided by CoinGecko API | Crypto Risk Management Dashboard")

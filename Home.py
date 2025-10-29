import streamlit as st
import pandas as pd
from pycoingecko import CoinGeckoAPI
import time
from datetime import datetime
from helpers.theme_config import Theme, create_theme_toggle, create_gradient_header
from helpers.i18n import I18n, t, create_language_selector

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Crypto Risk Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply theme
theme = Theme.apply_theme()

# Initialize CoinGecko API client
cg = CoinGeckoAPI()

def style_dataframe(df):
    """
    Apply custom styling to the dataframe.
    - Format numbers with commas and decimals.
    - Color '7d Change (%)' based on value.
    - Center align all content.
    """
    def color_change(val):
        """
        Colors positive values green and negative values red.
        """
        color = 'green' if val > 0 else 'red' if val < 0 else 'white'
        return f'color: {color}'

    styler = df.style.format({
        'Price (USD)': '$ {:,.2f}',
        'Market Cap (USD)': '$ {:,}',
        '7d Change (%)': '{:,.2f}%',
        'Circulating Supply': '{:,.0f}',
        'Total Supply': '{:,.0f}',
        'Max Supply': '{:,.0f}',
        'ATH (USD)': '$ {:,.2f}',
        'ATH Change (%)': '{:,.2f}%'
    }).map(color_change, subset=['7d Change (%)', 'ATH Change (%)']).set_properties(**{'text-align': 'center'})
    
    return styler

def get_top_coins_data():
    """
    Fetch top 500 coins market data from CoinGecko in pages.
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Fetch market data for top 500 coins in five pages
            all_markets = []
            for page_num in range(1, 6):  # Pages 1-5 for 500 coins
                markets = cg.get_coins_markets(
                    vs_currency='usd',
                    order='market_cap_desc',
                    per_page=100,
                    page=page_num,
                    sparkline=False,
                    price_change_percentage='7d'
                )
                all_markets.extend(markets)
                # Small delay between requests to avoid rate limiting
                time.sleep(0.1)
            
            # Process the data into a DataFrame
            coins_data = []
            for coin in all_markets:
                coins_data.append({
                    'Rank': coin['market_cap_rank'],
                    'Name': coin['name'],
                    'Symbol': coin['symbol'].upper(),
                    'Price (USD)': coin['current_price'],
                    'Market Cap (USD)': coin['market_cap'],
                    '7d Change (%)': coin.get('price_change_percentage_7d_in_currency', 0),
                    'Circulating Supply': coin.get('circulating_supply', 0),
                    'Total Supply': coin.get('total_supply', 0),
                    'Max Supply': coin.get('max_supply', 0),
                    'ATH (USD)': coin.get('ath', 0),
                    'ATH Date': pd.to_datetime(coin.get('ath_date')).strftime('%Y-%m-%d'),
                    'ATH Change (%)': coin.get('ath_change_percentage', 0)
                })
            
            df = pd.DataFrame(coins_data)
            return df
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:  # Rate limit error
                wait_time = 2 ** attempt  # Exponential backoff
                st.warning(f"Rate limited, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            st.error(f"Failed to fetch data from CoinGecko: {e}")
            return pd.DataFrame()

# Sidebar settings
with st.sidebar:
    st.header("⚙️ " + t('settings'))
    create_language_selector()
    st.markdown("---")
    create_theme_toggle()

# Header with gradient
create_gradient_header(
    t('welcome_message'),
    "Use the navigation to access Dashboard, Comparison, and Portfolio tools"
)

st.subheader("Live Market Data")

# Add controls for data refresh and display
col1, col2, col3 = st.columns(3)
with col1:
    height_slider = st.slider("Adjust Table Height", min_value=200, max_value=1000, value=500, step=50)
with col2:
    num_coins = st.selectbox("Number of Coins", [50, 100, 200, 300, 500], index=1)
with col3:
    auto_refresh = st.checkbox("Auto-refresh (20 min)", value=False)

# Add manual refresh button
if st.button("🔄 " + t('refresh'), type="primary"):
    st.cache_data.clear()
    st.rerun()

# Display last update time
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

st.caption(f"{t('last_updated')}: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

# Fetch and display data
with st.spinner("Fetching live market data from CoinGecko..."):
    # Modified function call to fetch configurable number of coins
    max_retries = 3
    all_markets = []
    
    for attempt in range(max_retries):
        try:
            cg = CoinGeckoAPI()
            # Calculate pages needed
            pages_needed = (num_coins + 99) // 100
            
            for page_num in range(1, pages_needed + 1):
                markets = cg.get_coins_markets(
                    vs_currency='usd',
                    order='market_cap_desc',
                    per_page=min(100, num_coins - len(all_markets)),
                    page=page_num,
                    sparkline=False,
                    price_change_percentage='7d'
                )
                all_markets.extend(markets)
                if len(all_markets) >= num_coins:
                    break
                time.sleep(0.1)
            
            # Process the data into a DataFrame
            coins_data = []
            for coin in all_markets[:num_coins]:
                coins_data.append({
                    'Rank': coin['market_cap_rank'],
                    'Name': coin['name'],
                    'Symbol': coin['symbol'].upper(),
                    'Price (USD)': coin['current_price'],
                    'Market Cap (USD)': coin['market_cap'],
                    '7d Change (%)': coin.get('price_change_percentage_7d_in_currency', 0),
                    'Circulating Supply': coin.get('circulating_supply', 0),
                    'Total Supply': coin.get('total_supply', 0),
                    'Max Supply': coin.get('max_supply', 0),
                    'ATH (USD)': coin.get('ath', 0),
                    'ATH Date': pd.to_datetime(coin.get('ath_date')).strftime('%Y-%m-%d') if coin.get('ath_date') else 'N/A',
                    'ATH Change (%)': coin.get('ath_change_percentage', 0)
                })
            
            top_coins_df = pd.DataFrame(coins_data)
            st.session_state.last_update = datetime.now()
            break
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait_time = 2 ** attempt
                st.warning(f"Rate limited, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            st.error(f"Failed to fetch data from CoinGecko: {e}")
            top_coins_df = pd.DataFrame()

if not top_coins_df.empty:
    # Apply styling
    styled_df = style_dataframe(top_coins_df)
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        height=height_slider
    )
else:
    st.warning("No data available. Please try refreshing in a few moments.")

# Auto-refresh implementation (non-blocking)
if auto_refresh:
    time.sleep(1)  # Small delay to prevent UI freezing
    st.info("Auto-refresh enabled. Page will refresh every 20 minutes.")
    # Use Streamlit's built-in auto-rerun feature with a timer
    if 'auto_refresh_counter' not in st.session_state:
        st.session_state.auto_refresh_counter = 0
    
    # Check if 20 minutes have passed
    if st.session_state.last_update:
        time_diff = datetime.now() - st.session_state.last_update
        if time_diff.total_seconds() >= 1200:  # 20 minutes
            st.rerun()

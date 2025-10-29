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

# Import helpers with error handling
try:
    from helpers.theme_config import Theme
except ImportError:
    Theme = None
    st.warning("Theme configuration not available")

try:
    from helpers.i18n import I18n, t
except ImportError:
    # Fallback function if i18n not available
    def t(key):
        translations = {
            'welcome_message': 'Welcome to Crypto Risk Dashboard',
            'settings': 'Settings',
            'language': 'Language',
            'theme': 'Theme',
            'refresh': 'Refresh',
            'last_updated': 'Last updated'
        }
        return translations.get(key, key)
    st.warning("Internationalization not available, using English")

try:
    from helpers.modern_ui import (
        ModernUI, 
        create_modern_sidebar, 
        create_modern_header,
        create_glass_card,
        create_modern_metric_card,
        apply_light_mode_fix
    )
except ImportError as e:
    ModernUI = None
    create_modern_sidebar = None
    create_modern_header = None
    apply_light_mode_fix = None
    st.warning(f"Modern UI not available: {e}")

try:
    from helpers.svg_icons import get_svg_icon
except ImportError as e:
    def get_svg_icon(name, size=24, color=None):
        return ""
    st.warning(f"SVG icons not available: {e}")

# Apply modern theme if available
if ModernUI:
    try:
        ModernUI.apply_modern_theme()
    except Exception as e:
        st.error(f"Error applying theme: {e}")
else:
    # Apply basic theme as fallback
    if Theme:
        Theme.apply_theme()

# Apply light mode text fix
if apply_light_mode_fix:
    try:
        apply_light_mode_fix()
    except Exception as e:
        st.error(f"Error applying light mode fix: {e}")

# Initialize CoinGecko API client
cg = CoinGeckoAPI()

def style_dataframe(df):
    """
    Apply custom styling to the dataframe.
    - Format numbers with commas and decimals.
    - Color '7d Change (%)' based on value (only in dark mode).
    - Center align all content.
    """
    # Check current theme
    current_theme = st.session_state.get('theme', 'dark')
    
    def color_change(val):
        """
        Colors positive values green and negative values red.
        Only applies in dark mode for visibility.
        """
        if current_theme == 'light':
            # In light mode, use black text for all values
            return 'color: #000000'
        else:
            # In dark mode, use colored text
            color = 'green' if val > 0 else 'red' if val < 0 else 'white'
            return f'color: {color}'

    # Format numbers first
    styler = df.style.format({
        'Price (USD)': '$ {:,.2f}',
        'Market Cap (USD)': '$ {:,}',
        '7d Change (%)': '{:,.2f}%',
        'Circulating Supply': '{:,.0f}',
        'Total Supply': '{:,.0f}',
        'Max Supply': '{:,.0f}',
        'ATH (USD)': '$ {:,.2f}',
        'ATH Change (%)': '{:,.2f}%'
    })
    
    # Only apply color mapping in dark mode
    if current_theme == 'dark':
        styler = styler.map(color_change, subset=['7d Change (%)', 'ATH Change (%)'])
    
    # Set text alignment for all cells
    styler = styler.set_properties(**{'text-align': 'center'})
    
    # In light mode, force all text to be black
    if current_theme == 'light':
        styler = styler.set_properties(**{'color': '#000000', 'background-color': '#ffffff'})
    
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

# Create sidebar with fallback
if create_modern_sidebar:
    try:
        create_modern_sidebar()
    except Exception as e:
        st.sidebar.error(f"Error creating sidebar: {e}")
        # Fallback sidebar
        with st.sidebar:
            st.header("⚙️ Settings")
else:
    # Fallback sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

# Create header with fallback
if create_modern_header:
    try:
        create_modern_header(
            t('welcome_message'),
            "Professional cryptocurrency risk management and analytics platform",
            icon="chart"
        )
    except Exception as e:
        st.error(f"Error creating header: {e}")
        # Fallback header
        st.title("📊 Crypto Risk Dashboard")
        st.markdown("Professional cryptocurrency risk management and analytics platform")
else:
    # Fallback header
    st.title("📊 Crypto Risk Dashboard")
    st.markdown("Professional cryptocurrency risk management and analytics platform")

# Live Market Data Section
market_header = f"""
<div style="display: flex; align-items: center; gap: 0.75rem; margin: 2rem 0 1rem 0;">
    {get_svg_icon('analytics', size=24)}
    <h2 style="margin: 0; font-weight: 600;">Live Market Data</h2>
</div>
"""
st.markdown(market_header, unsafe_allow_html=True)

# Controls in a glass card
controls_html = f"""
<div class="glass-card" style="margin-bottom: 1.5rem;">
    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
        {get_svg_icon('settings', size=20)}
        <h3 style="margin: 0; font-weight: 600;">Display Controls</h3>
    </div>
</div>
"""
st.markdown(controls_html, unsafe_allow_html=True)

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
    # Modern refresh button
    if st.button(
        "↻ " + t('refresh'), 
        type="primary", 
        use_container_width=True,
        help="Manually refresh market data"
    ):
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

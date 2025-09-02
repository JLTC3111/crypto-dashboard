import streamlit as st
import pandas as pd
from pycoingecko import CoinGeckoAPI
import time

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Crypto Risk Dashboard",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    Fetch top 200 coins market data from CoinGecko in pages.
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Fetch market data for top 200 coins in two pages
            all_markets = []
            for page_num in [1, 2]:
                markets = cg.get_coins_markets(
                    vs_currency='usd',
                    order='market_cap_desc',
                    per_page=100,
                    page=page_num,
                    sparkline=False,
                    price_change_percentage='7d'
                )
                all_markets.extend(markets)
            
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

# Duplicate page config removed - already set at the top of the file

st.title("Crypto Risk Management Dashboard")

st.markdown("""
Welcome to the Crypto Risk Management Dashboard. Use the navigation on the left to access the **Dashboard** and **Comparison** tools.
""")

st.subheader("Live Market Data (Top 200 Coins)")

height_slider = st.slider("Adjust Table Height", min_value=200, max_value=1000, value=500, step=50)

placeholder = st.empty()

# loop to auto-refresh
while True:
    with placeholder.container():
        with st.spinner("Fetching live market data from CoinGecko..."):
            top_coins_df = get_top_coins_data()

        if not top_coins_df.empty:
            # Apply styling
            styled_df = style_dataframe(top_coins_df)
            
            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True,
                height=height_slider
            )
    time.sleep(1200)
    st.rerun()

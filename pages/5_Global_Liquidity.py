"""
Global Liquidity Tracker Page
Displays macro liquidity metrics with traffic-light scoring for crypto investment decisions
"""

import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Import the liquidity tracker
from helpers.liquidity_tracker import (
    GlobalLiquidityTracker, 
    format_metric_value, 
    get_status_color, 
    get_status_emoji
)
from supabase_config import require_auth

try:
    from helpers.modern_ui import apply_dropdown_fix
except ImportError:
    apply_dropdown_fix = None

# Page configuration
st.set_page_config(
    page_title="Global Liquidity Tracker",
    page_icon="🌊",
    layout="wide"
)

# Apply light mode text fix
if apply_dropdown_fix:
    apply_dropdown_fix()

# Custom CSS
st.markdown("""
<style>
    .liquidity-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #ddd;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card.green {
        border-left-color: #28a745;
    }
    .metric-card.amber {
        border-left-color: #ffc107;
    }
    .metric-card.red {
        border-left-color: #dc3545;
    }
    .status-indicator {
        font-size: 1.2em;
        font-weight: bold;
    }
    .overall-score {
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
    }
    .overall-score.green {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
    }
    .overall-score.amber {
        background: linear-gradient(135deg, #ffc107, #fd7e14);
        color: white;
    }
    .overall-score.red {
        background: linear-gradient(135deg, #dc3545, #e83e8c);
        color: white;
    }
    .interpretation-box {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    .data-source {
        font-size: 0.8em;
        color: #6c757d;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Require authentication
if not require_auth():
    st.stop()

# Header
st.markdown("""
<div class="liquidity-header">
    <h1>🌊 Global Liquidity Tracker</h1>
    <p>Real-time macro liquidity metrics with traffic-light scoring for crypto investment decisions</p>
</div>
""", unsafe_allow_html=True)

# Initialize tracker
@st.cache_resource
def get_liquidity_tracker():
    return GlobalLiquidityTracker()

tracker = get_liquidity_tracker()

# Main content
with st.container():
    # Refresh controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader("📊 Liquidity Health Dashboard")
    
    with col2:
        if st.button("🔄 Refresh Data", help="Update all metrics"):
            st.cache_data.clear()
            st.rerun()
    
    with col3:
        auto_refresh = st.checkbox("⚡ Auto-refresh", help="Refresh data every 5 minutes")

    # Fetch metrics
    with st.spinner("Loading liquidity metrics..."):
        metrics = tracker.get_all_metrics()
        overall_status, overall_score = tracker.calculate_overall_liquidity_score(metrics)

    # Overall Score Display
    st.markdown(f"""
    <div class="overall-score {overall_status}">
        <div>Overall Liquidity Health</div>
        <div>{overall_score}/100</div>
        <div style="font-size: 0.6em; margin-top: 10px;">
            {get_status_emoji(overall_status)} {overall_status.upper()} SIGNAL
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Data Freshness Summary
    if metrics:
        latest_data_dates = []
        fetch_time = datetime.now()  # Default fallback
        for metric in metrics.values():
            latest_data_dates.append(metric.last_updated)
            fetch_time = metric.fetched_at  # Use the actual fetch time
        
        oldest_data = min(latest_data_dates)
        newest_data = max(latest_data_dates)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📅 Data Range", f"{oldest_data.strftime('%b %d')} - {newest_data.strftime('%b %d, %Y')}")
        with col2:
            st.metric("🕐 Last Fetch", fetch_time.strftime('%H:%M UTC'))
        with col3:
            st.metric("📊 Metrics", f"{len(metrics)} sources")

    # Key Metrics Cards
    st.subheader("📈 Key Liquidity Metrics")
    
    # Create metric cards in columns
    cols = st.columns(3)
    metric_items = list(metrics.items())
    
    for i, (key, metric) in enumerate(metric_items):
        col_idx = i % 3
        
        with cols[col_idx]:
            # Calculate change indicator
            if metric.change > 0:
                change_indicator = f"↗️ +{metric.change:.2f}"
                change_color = "green"
            elif metric.change < 0:
                change_indicator = f"↘️ {metric.change:.2f}"
                change_color = "red"
            else:
                change_indicator = "➡️ 0.00"
                change_color = "gray"
            
            st.markdown(f"""
            <div class="metric-card {metric.status}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="margin-bottom: 6px;">
                            <span style="background: #e9ecef; padding: 3px 8px; border-radius: 4px; font-size: 0.75em; font-weight: bold; color: #495057; margin-right: 8px;">{metric.label}</span>
                        </div>
                        <h4 style="margin: 0 0 8px 0; font-size: 0.95em; color: #343a40; line-height: 1.2;">{metric.name}</h4>
                        <div style="font-size: 1.3em; font-weight: bold; margin: 5px 0;">
                            {format_metric_value(metric.value, metric.unit)}
                        </div>
                        <div style="font-size: 0.8em; color: {change_color};">
                            {change_indicator}
                        </div>
                        <div class="data-source">
                            <strong>Data:</strong> {metric.last_updated.strftime('%b %d, %Y')}<br>
                            <strong>Fetched:</strong> {metric.fetched_at.strftime('%b %d, %Y %H:%M UTC')} | {metric.source}
                        </div>
                    </div>
                    <div class="status-indicator" style="color: {get_status_color(metric.status)};">
                        {get_status_emoji(metric.status)}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Detailed Analysis Section
    st.markdown("---")
    st.subheader("🔍 Detailed Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Charts", "📋 Interpretation", "⚙️ Methodology", "📡 Data Sources"])
    
    with tab1:
        st.markdown("### Historical Trends")
        
        # Create charts for key metrics
        if metrics:
            # Sample chart - in real implementation, you'd fetch historical data
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=['M2 Money Supply', 'Bank Reserves', 'Treasury Yields', 'Crypto Metrics'],
                specs=[[{'secondary_y': False}, {'secondary_y': False}],
                       [{'secondary_y': False}, {'secondary_y': False}]]
            )
            
            # Mock historical data for demonstration
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
            
            # M2 trend
            m2_values = 21000 + (dates - dates[0]).days * 10 + pd.Series(range(30)).apply(lambda x: x * 0.1)
            fig.add_trace(
                go.Scatter(x=dates, y=m2_values, name='M2 Supply', line=dict(color='blue')),
                row=1, col=1
            )
            
            # Bank reserves trend
            reserves_values = 3200 + pd.Series(range(30)).apply(lambda x: x * 5)
            fig.add_trace(
                go.Scatter(x=dates, y=reserves_values, name='Bank Reserves', line=dict(color='green')),
                row=1, col=2
            )
            
            # Yield trends
            yield_10y = 4.5 + pd.Series(range(30)).apply(lambda x: (x-15) * 0.02)
            yield_2y = 4.0 + pd.Series(range(30)).apply(lambda x: (x-15) * 0.03)
            fig.add_trace(
                go.Scatter(x=dates, y=yield_10y, name='10Y Yield', line=dict(color='red')),
                row=2, col=1
            )
            fig.add_trace(
                go.Scatter(x=dates, y=yield_2y, name='2Y Yield', line=dict(color='orange')),
                row=2, col=1
            )
            
            # Crypto metrics
            stablecoin_supply = 125 + pd.Series(range(30)).apply(lambda x: x * 0.5)
            defi_tvl = 45 + pd.Series(range(30)).apply(lambda x: x * 0.3)
            fig.add_trace(
                go.Scatter(x=dates, y=stablecoin_supply, name='Stablecoin Supply', line=dict(color='purple')),
                row=2, col=2
            )
            fig.add_trace(
                go.Scatter(x=dates, y=defi_tvl, name='DeFi TVL', line=dict(color='cyan')),
                row=2, col=2
            )
            
            fig.update_layout(height=600, showlegend=True, title_text="Liquidity Metrics Trends")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Current Market Interpretation")
        
        # Generate interpretation based on overall score
        if overall_score >= 70:
            interpretation_color = "success"
            interpretation_title = "🟢 Positive Liquidity Environment"
            interpretation_text = """
            **Strong liquidity conditions detected:**
            - Central bank money supply is expanding
            - Bank reserves are increasing
            - Bond yields trending downward (supportive of risk assets)
            - Crypto-specific metrics showing growth
            
            **Investment Implications:**
            - Favorable environment for crypto and risk assets
            - Increased institutional and retail liquidity
            - Consider increasing portfolio exposure
            """
        elif overall_score >= 40:
            interpretation_color = "warning"
            interpretation_title = "🟡 Mixed Liquidity Signals"
            interpretation_text = """
            **Neutral to mixed liquidity conditions:**
            - Some metrics showing positive trends, others neutral/negative
            - Market transition period or consolidation phase
            - Increased volatility possible
            
            **Investment Implications:**
            - Maintain current portfolio allocation
            - Monitor for clearer directional signals
            - Consider defensive positioning
            """
        else:
            interpretation_color = "danger"
            interpretation_title = "🔴 Constrained Liquidity Environment"
            interpretation_text = """
            **Liquidity conditions tightening:**
            - Money supply growth slowing or contracting
            - Rising interest rates reducing liquidity
            - Risk-off sentiment in markets
            
            **Investment Implications:**
            - Consider reducing risk asset exposure
            - Increase cash/stable asset allocation
            - Focus on quality and defensive positions
            """
        
        st.markdown(f"""
        <div class="interpretation-box">
            <h4>{interpretation_title}</h4>
            {interpretation_text}
        </div>
        """, unsafe_allow_html=True)
        
        # Specific metric insights
        st.markdown("### Metric-Specific Insights")
        
        insights_data = []
        for key, metric in metrics.items():
            if metric.status == 'green':
                insight = f"✅ {metric.name}: Supportive for risk assets"
            elif metric.status == 'red':
                insight = f"⚠️ {metric.name}: Headwind for risk assets"
            else:
                insight = f"➖ {metric.name}: Neutral impact"
            
            insights_data.append({
                'Metric': metric.name,
                'Status': f"{get_status_emoji(metric.status)} {metric.status.upper()}",
                'Value': format_metric_value(metric.value, metric.unit),
                'Data Date': metric.last_updated.strftime('%b %d, %Y'),
                'Fetched': metric.fetched_at.strftime('%H:%M UTC'),
                'Insight': insight
            })
        
        insights_df = pd.DataFrame(insights_data)
        st.dataframe(insights_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### Scoring Methodology")
        
        st.markdown("""
        #### Traffic Light System
        
        Each metric is assigned a color based on predefined thresholds that indicate liquidity conditions:
        
        **🟢 Green (Positive for Crypto):**
        - M2: >0.1% week-over-week growth
        - Bank Reserves: >$25B weekly increase  
        - RRP Usage: <$300B (cash in markets)
        - Bond Yields: Trending downward (4-week)
        - Stablecoin Supply: >1% growth (14-day)
        - DeFi TVL: >5% growth (14-day)
        
        **🟡 Amber (Neutral):**
        - Metrics showing minimal change or mixed signals
        - Transitional periods between bullish/bearish regimes
        
        **🔴 Red (Negative for Crypto):**
        - M2: Declining week-over-week
        - Bank Reserves: >$25B weekly decrease
        - RRP Usage: >$800B (cash parked at Fed)
        - Bond Yields: Trending upward
        - Stablecoin Supply: Declining
        - DeFi TVL: Declining >5%
        
        #### Overall Score Calculation
        - Each green metric = +1 point
        - Each amber metric = 0 points  
        - Each red metric = -1 point
        - Score normalized to 0-100 scale
        - 70+ = Bullish liquidity environment
        - 40-69 = Neutral/Mixed signals
        - <40 = Bearish liquidity environment
        """)
    
    with tab4:
        st.markdown("### Data Sources & Update Frequency")
        
        sources_data = [
            {
                'Metric': 'M2 Money Supply',
                'Source': 'FRED (Federal Reserve Economic Data)',
                'API': 'M2SL series (seasonally adjusted)',
                'Data Publication': 'Monthly (typically ~2 months delay)',
                'Analysis Period': 'Weekly comparison',
                'Free Access': '✅'
            },
            {
                'Metric': 'Bank Reserve Balances',
                'Source': 'FRED',
                'API': 'WRESBAL series (Total Reserves)',
                'Data Publication': 'Weekly (Thursday)',
                'Analysis Period': 'Weekly comparison',
                'Free Access': '✅'
            },
            {
                'Metric': 'Reverse Repo Usage',
                'Source': 'FRED / NY Fed',
                'API': 'RRPONTSYD series',
                'Data Publication': 'Daily',
                'Analysis Period': 'Current level',
                'Free Access': '✅'
            },
            {
                'Metric': 'Treasury Yields',
                'Source': 'FRED',
                'API': 'DGS2, DGS10 series',
                'Data Publication': 'Daily',
                'Analysis Period': '4-week trend',
                'Free Access': '✅'
            },
            {
                'Metric': 'Stablecoin Market Cap',
                'Source': 'CoinGecko',
                'API': 'Public API',
                'Data Publication': 'Real-time',
                'Analysis Period': 'Current level',
                'Free Access': '✅'
            },
            {
                'Metric': 'DeFi TVL',
                'Source': 'DeFiLlama',
                'API': 'Public API',
                'Data Publication': 'Real-time',
                'Analysis Period': 'Current level',
                'Free Access': '✅'
            }
        ]
        
        sources_df = pd.DataFrame(sources_data)
        st.dataframe(sources_df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        #### Data Timing Explanation
        
        **📅 Data Date vs 📡 Fetch Time:**
        - **Data Date**: When the underlying economic data was actually observed/published
        - **Fetch Time**: When our system retrieved the data from the API
        
        **⏰ Why the Delay?**
        - **M2 Money Supply**: Published monthly with ~2 month delay (e.g., June data available in August)
        - **Bank Reserves**: Published weekly on Thursdays for the previous week
        - **Treasury Yields & RRP**: Published daily with 1-day delay
        - **Crypto Metrics**: Real-time data, so observation date = fetch time
        
        This is normal for economic data - official statistics take time to compile and verify.
        """)
        
        st.markdown("""
        #### API Configuration
        
        To enable full functionality, add your FRED API key to `secrets.toml`:
        
        ```toml
        [apis]
        fred_api_key = "your_fred_api_key_here"
        ```
        
        **Get a free FRED API key:**
        1. Visit [https://fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html)
        2. Create an account
        3. Request an API key (instant approval)
        4. Add to your secrets.toml file
        
        **Note:** Other APIs (CoinGecko, DeFiLlama) don't require keys for basic usage.
        """)

# Auto-refresh functionality
if auto_refresh:
    time.sleep(300)  # 5 minutes
    st.rerun()

# Footer
st.markdown("---")
st.caption("""
🌊 Global Liquidity Tracker | Data sources: FRED, CoinGecko, DeFiLlama | 
Not financial advice - for informational purposes only
""")

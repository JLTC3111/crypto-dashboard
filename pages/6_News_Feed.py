import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
from helpers.news_feed import CryptoNewsFeed, PremiumNewsSources

st.set_page_config(
    page_title="Crypto News Feed",
    page_icon="📰",
    layout="wide"
)

def main():
    st.title("📰 Crypto News Feed & Impact Analysis")
    st.markdown("Real-time crypto news from major sources with AI-powered impact analysis")
    
    # Initialize news feed
    if 'news_feed' not in st.session_state:
        st.session_state.news_feed = CryptoNewsFeed()
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ News Settings")
        
        # Refresh controls
        if st.button("🔄 Refresh News", type="primary"):
            st.cache_data.clear()
            st.rerun()
        
        # Filter controls
        st.subheader("Filters")
        max_articles = st.slider("Max Articles", 10, 100, 50)
        min_impact = st.slider("Minimum Impact Rating", 1, 10, 1)
        
        # Time filter
        time_filter = st.selectbox(
            "Time Range",
            ["All", "Last 24 hours", "Last 3 days", "Last week"]
        )
        
        # Source filter
        sources = ["All", "CoinDesk", "Cointelegraph", "The Block", "CryptoSlate", "Decrypt"]
        selected_sources = st.multiselect("Sources", sources, default=["All"])
        if "All" in selected_sources:
            selected_sources = sources[1:]  # Exclude "All" from actual filtering
        
        # Auto-refresh
        auto_refresh = st.checkbox("Auto-refresh (5 min)")
        if auto_refresh:
            st.info("Auto-refresh enabled")
    
    # Fetch news
    with st.spinner("Fetching latest crypto news..."):
        try:
            articles = st.session_state.news_feed.fetch_news(max_articles)
            
            # Apply filters
            filtered_articles = []
            cutoff_time = datetime.now()
            
            if time_filter == "Last 24 hours":
                cutoff_time = datetime.now() - timedelta(days=1)
            elif time_filter == "Last 3 days":
                cutoff_time = datetime.now() - timedelta(days=3)
            elif time_filter == "Last week":
                cutoff_time = datetime.now() - timedelta(weeks=1)
            
            for article in articles:
                # Apply filters
                if article.impact_rating < min_impact:
                    continue
                if time_filter != "All" and article.published < cutoff_time:
                    continue
                if selected_sources and article.source not in selected_sources:
                    continue
                
                filtered_articles.append(article)
            
            articles = filtered_articles
            
        except Exception as e:
            st.error(f"Failed to fetch news: {str(e)}")
            articles = []
    
    if not articles:
        st.warning("No articles found matching your criteria.")
        return
    
    # Impact Summary Dashboard
    st.header("📊 Market Impact Overview")
    
    impact_summary = st.session_state.news_feed.get_impact_summary(articles)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Average Impact",
            f"{impact_summary['avg_impact']}/10",
            delta=None
        )
    
    with col2:
        st.metric(
            "High Impact Articles",
            impact_summary['high_impact_count'],
            delta=None
        )
    
    with col3:
        st.metric(
            "Market Sentiment",
            impact_summary['market_sentiment'],
            delta=None
        )
    
    with col4:
        st.metric(
            "Total Articles",
            len(articles),
            delta=None
        )
    
    # Impact distribution chart
    col1, col2 = st.columns(2)
    
    with col1:
        # Impact rating distribution
        impact_counts = {}
        for article in articles:
            impact_counts[article.impact_rating] = impact_counts.get(article.impact_rating, 0) + 1
        
        if impact_counts:
            fig_impact = px.bar(
                x=list(impact_counts.keys()),
                y=list(impact_counts.values()),
                title="Impact Rating Distribution",
                labels={'x': 'Impact Rating', 'y': 'Number of Articles'},
                color=list(impact_counts.values()),
                color_continuous_scale='Reds'
            )
            fig_impact.update_layout(height=300)
            st.plotly_chart(fig_impact, use_container_width=True, key="impact_distribution_chart")
    
    with col2:
        # Source distribution
        source_counts = {}
        for article in articles:
            source_counts[article.source] = source_counts.get(article.source, 0) + 1
        
        if source_counts:
            fig_sources = px.pie(
                values=list(source_counts.values()),
                names=list(source_counts.keys()),
                title="Articles by Source"
            )
            fig_sources.update_layout(height=300)
            st.plotly_chart(fig_sources, use_container_width=True, key="source_distribution_chart")
    
    # Top keywords
    if impact_summary['top_keywords']:
        st.subheader("🔥 Trending Keywords")
        keyword_cols = st.columns(5)
        for i, (keyword, count) in enumerate(impact_summary['top_keywords'][:5]):
            with keyword_cols[i % 5]:
                st.metric(keyword.title(), count)
    
    # News articles
    st.header("📰 Latest News Articles")
    
    # Sort options
    sort_by = st.selectbox(
        "Sort by:",
        ["Impact Rating (High to Low)", "Publication Date (Newest)", "Impact Rating (Low to High)"]
    )
    
    if sort_by == "Impact Rating (High to Low)":
        articles.sort(key=lambda x: x.impact_rating, reverse=True)
    elif sort_by == "Impact Rating (Low to High)":
        articles.sort(key=lambda x: x.impact_rating)
    else:  # Publication Date
        articles.sort(key=lambda x: x.published, reverse=True)
    
    # Display articles
    for i, article in enumerate(articles):
        with st.expander(
            f"{'🔥' if article.impact_rating >= 8 else '⚠️' if article.impact_rating >= 6 else '📄'} "
            f"[{article.impact_rating}/10] {article.title}",
            expanded=(i < 3)  # Expand first 3 articles
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Source:** {article.source}")
                st.markdown(f"**Published:** {article.published.strftime('%Y-%m-%d %H:%M')}")
                st.markdown(f"**Summary:** {article.summary}")
                
                if article.keywords:
                    keywords_str = ", ".join([f"`{kw}`" for kw in article.keywords[:10]])
                    st.markdown(f"**Keywords:** {keywords_str}")
                
                st.markdown(f"**[Read Full Article]({article.url})**")
            
            with col2:
                # Impact rating gauge
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = article.impact_rating,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Impact Rating"},
                    gauge = {
                        'axis': {'range': [None, 10]},
                        'bar': {'color': "darkred" if article.impact_rating >= 8 else "orange" if article.impact_rating >= 6 else "green"},
                        'steps': [
                            {'range': [0, 3], 'color': "lightgray"},
                            {'range': [3, 6], 'color': "yellow"},
                            {'range': [6, 10], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 8
                        }
                    }
                ))
                fig_gauge.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig_gauge, use_container_width=True, key=f"gauge_chart_{i}")
            
            # Impact analysis
            st.markdown("### 📈 Impact Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Short-term Impact:**")
                st.info(article.short_term_impact)
            
            with col2:
                st.markdown("**Long-term Impact:**")
                st.info(article.long_term_impact)
            
            st.divider()
    
    # Additional premium sources
    with st.expander("🔒 Premium Sources (Requires API Keys)"):
        st.markdown("""
        **Additional news sources available with API keys:**
        
        - **Messari**: High-quality research and market intelligence
        - **Bloomberg Terminal**: Professional-grade financial news
        - **Reuters Eikon**: Institutional news and analysis
        
        Configure API keys in your Streamlit secrets to access these sources.
        """)
        
        # Show any available premium content
        try:
            financial_articles = PremiumNewsSources.get_financial_media_feeds()
            if financial_articles:
                st.subheader("Financial Media Crypto Coverage")
                for article in financial_articles[:5]:
                    st.markdown(f"- **[{article['title']}]({article['url']})** - *{article['source']}*")
        except:
            pass
    
    # Auto-refresh mechanism
    if auto_refresh:
        import time
        time.sleep(300)  # 5 minutes
        st.rerun()

if __name__ == "__main__":
    main()

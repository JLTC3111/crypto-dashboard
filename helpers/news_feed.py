import requests
import feedparser
import re
import ssl
import urllib.request
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import streamlit as st
from dataclasses import dataclass
import time

# Fix SSL certificate issues on macOS
ssl._create_default_https_context = ssl._create_unverified_context

@dataclass
class NewsArticle:
    title: str
    summary: str
    url: str
    source: str
    published: datetime
    impact_rating: int
    short_term_impact: str
    long_term_impact: str
    keywords: List[str]

class CryptoNewsFeed:
    def __init__(self):
        self.sources = {
            'coindesk': {
                'name': 'CoinDesk',
                'rss_url': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
                'weight': 0.9,  # Editorial quality weight
                'type': 'rss'
            },
            'cointelegraph': {
                'name': 'Cointelegraph',
                'rss_url': 'https://cointelegraph.com/rss',
                'weight': 0.8,
                'type': 'rss'
            },
            'theblock': {
                'name': 'The Block',
                'rss_url': 'https://www.theblock.co/rss.xml',
                'weight': 0.95,  # High weight for institutional insights
                'type': 'rss'
            },
            'cryptoslate': {
                'name': 'CryptoSlate',
                'rss_url': 'https://cryptoslate.com/feed/',
                'weight': 0.7,
                'type': 'rss'
            },
            'decrypt': {
                'name': 'Decrypt',
                'rss_url': 'https://decrypt.co/feed',
                'weight': 0.75,
                'type': 'rss'
            }
        }
        
        # Keywords for impact analysis
        self.high_impact_keywords = [
            'regulation', 'sec', 'cftc', 'fed', 'federal reserve', 'ban', 'lawsuit',
            'hack', 'exploit', 'crash', 'surge', 'etf', 'institutional', 'adoption',
            'bitcoin', 'ethereum', 'stablecoin', 'cbdc', 'interest rates', 'inflation'
        ]
        
        self.medium_impact_keywords = [
            'partnership', 'integration', 'upgrade', 'fork', 'defi', 'nft', 'web3',
            'mining', 'staking', 'yield', 'liquidity', 'trading volume', 'market cap'
        ]
        
        self.low_impact_keywords = [
            'conference', 'interview', 'opinion', 'analysis', 'prediction', 'tutorial',
            'guide', 'review', 'comparison', 'announcement'
        ]

    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def fetch_news(_self, max_articles: int = 50) -> List[NewsArticle]:
        """Fetch news from all configured sources"""
        all_articles = []
        
        for source_id, source_config in _self.sources.items():
            try:
                articles = _self._fetch_from_rss(source_config, max_articles // len(_self.sources))
                all_articles.extend(articles)
            except Exception as e:
                st.warning(f"Failed to fetch from {source_config['name']}: {str(e)}")
                continue
        
        # Sort by publication date (newest first)
        all_articles.sort(key=lambda x: x.published, reverse=True)
        
        return all_articles[:max_articles]

    def _fetch_from_rss(self, source_config: Dict, max_articles: int) -> List[NewsArticle]:
        """Fetch articles from RSS feed"""
        try:
            feed = feedparser.parse(source_config['rss_url'])
            articles = []
            
            for entry in feed.entries[:max_articles]:
                # Parse publication date
                try:
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        published = datetime(*entry.updated_parsed[:6])
                    else:
                        published = datetime.now()
                except:
                    published = datetime.now()
                
                # Get summary
                summary = ""
                if hasattr(entry, 'summary'):
                    summary = self._clean_html(entry.summary)
                elif hasattr(entry, 'description'):
                    summary = self._clean_html(entry.description)
                
                # Create article with analysis
                article = NewsArticle(
                    title=entry.title,
                    summary=summary,
                    url=entry.link,
                    source=source_config['name'],
                    published=published,
                    impact_rating=0,
                    short_term_impact="",
                    long_term_impact="",
                    keywords=[]
                )
                
                # Analyze impact
                self._analyze_impact(article, source_config['weight'])
                articles.append(article)
            
            return articles
            
        except Exception as e:
            raise Exception(f"RSS fetch failed: {str(e)}")

    def _clean_html(self, text: str) -> str:
        """Remove HTML tags and clean text"""
        if not text:
            return ""
        
        # Remove HTML tags
        clean = re.compile('<.*?>')
        text = re.sub(clean, '', text)
        
        # Clean up whitespace
        text = ' '.join(text.split())
        
        return text[:500]  # Limit summary length

    def _analyze_impact(self, article: NewsArticle, source_weight: float):
        """Analyze article impact and assign ratings"""
        text_to_analyze = f"{article.title} {article.summary}".lower()
        
        # Extract keywords
        found_keywords = []
        impact_score = 0
        
        # Check for high impact keywords
        for keyword in self.high_impact_keywords:
            if keyword in text_to_analyze:
                found_keywords.append(keyword)
                impact_score += 3
        
        # Check for medium impact keywords
        for keyword in self.medium_impact_keywords:
            if keyword in text_to_analyze:
                found_keywords.append(keyword)
                impact_score += 2
        
        # Check for low impact keywords
        for keyword in self.low_impact_keywords:
            if keyword in text_to_analyze:
                found_keywords.append(keyword)
                impact_score += 1
        
        # Apply source weight
        impact_score = int(impact_score * source_weight)
        
        # Cap at 10
        impact_score = min(impact_score, 10)
        
        article.keywords = found_keywords
        article.impact_rating = max(impact_score, 1)  # Minimum rating of 1
        
        # Generate impact analysis
        self._generate_impact_analysis(article)

    def _generate_impact_analysis(self, article: NewsArticle):
        """Generate short-term and long-term impact analysis"""
        keywords = article.keywords
        rating = article.impact_rating
        
        # Short-term impact analysis
        if rating >= 8:
            article.short_term_impact = "High volatility expected. Immediate market reaction likely within hours."
        elif rating >= 6:
            article.short_term_impact = "Moderate market movement possible. Watch for price action in 24-48 hours."
        elif rating >= 4:
            article.short_term_impact = "Limited immediate impact. May influence sentiment over 1-3 days."
        else:
            article.short_term_impact = "Minimal short-term market impact expected."
        
        # Long-term impact analysis
        regulatory_keywords = ['regulation', 'sec', 'cftc', 'ban', 'lawsuit', 'cbdc']
        institutional_keywords = ['institutional', 'etf', 'adoption', 'partnership']
        technical_keywords = ['upgrade', 'fork', 'hack', 'exploit']
        
        if any(kw in keywords for kw in regulatory_keywords):
            article.long_term_impact = "Regulatory developments may reshape market structure over months/years."
        elif any(kw in keywords for kw in institutional_keywords):
            article.long_term_impact = "Institutional involvement could drive sustained growth or legitimacy."
        elif any(kw in keywords for kw in technical_keywords):
            article.long_term_impact = "Technical changes may affect network security, scalability, or adoption."
        elif rating >= 6:
            article.long_term_impact = "Significant long-term implications for crypto market development."
        else:
            article.long_term_impact = "Limited long-term structural impact on crypto markets."

    def get_impact_summary(self, articles: List[NewsArticle]) -> Dict:
        """Generate overall impact summary from articles"""
        if not articles:
            return {
                'avg_impact': 0,
                'high_impact_count': 0,
                'top_keywords': [],
                'market_sentiment': 'Neutral'
            }
        
        # Calculate average impact
        avg_impact = sum(article.impact_rating for article in articles) / len(articles)
        
        # Count high impact articles
        high_impact_count = len([a for a in articles if a.impact_rating >= 7])
        
        # Get top keywords
        all_keywords = []
        for article in articles:
            all_keywords.extend(article.keywords)
        
        keyword_counts = {}
        for keyword in all_keywords:
            keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Determine market sentiment
        if avg_impact >= 7:
            sentiment = 'Highly Volatile'
        elif avg_impact >= 5:
            sentiment = 'Cautious'
        elif avg_impact >= 3:
            sentiment = 'Neutral'
        else:
            sentiment = 'Stable'
        
        return {
            'avg_impact': round(avg_impact, 1),
            'high_impact_count': high_impact_count,
            'top_keywords': top_keywords,
            'market_sentiment': sentiment
        }

# Additional news sources that require API keys or different approaches
class PremiumNewsSources:
    """Handler for premium news sources that may require API keys"""
    
    @staticmethod
    def get_messari_news(api_key: Optional[str] = None) -> List[Dict]:
        """Fetch from Messari API if available"""
        if not api_key:
            return []
        
        try:
            headers = {'x-messari-api-key': api_key}
            response = requests.get('https://data.messari.io/api/v1/news', headers=headers)
            if response.status_code == 200:
                return response.json().get('data', [])
        except:
            pass
        return []
    
    @staticmethod
    def get_financial_media_feeds() -> List[Dict]:
        """Get crypto news from traditional financial media RSS feeds"""
        feeds = {
            'Bloomberg Crypto': 'https://feeds.bloomberg.com/crypto/news.rss',
            'Reuters Crypto': 'https://feeds.reuters.com/reuters/technologyNews',
        }
        
        articles = []
        for source, url in feeds.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]:  # Limit to avoid overwhelming
                    if any(crypto_term in entry.title.lower() for crypto_term in 
                          ['crypto', 'bitcoin', 'ethereum', 'blockchain', 'digital currency']):
                        articles.append({
                            'title': entry.title,
                            'url': entry.link,
                            'source': source,
                            'published': entry.get('published', '')
                        })
            except:
                continue
        
        return articles

"""
Global Liquidity Tracker Module
Tracks macro liquidity metrics and provides traffic-light scoring for crypto portfolio decisions
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import numpy as np
from dataclasses import dataclass
import time

@dataclass
class LiquidityMetric:
    """Data class for liquidity metrics"""
    name: str
    label: str  # Short identifier/key for the metric
    value: float
    change: float
    status: str  # 'green', 'amber', 'red'
    last_updated: datetime  # Date of the actual data observation
    fetched_at: datetime   # Date/time when we retrieved it
    source: str
    unit: str

class GlobalLiquidityTracker:
    """Main class for tracking global liquidity metrics"""
    
    def __init__(self):
        self.cache_duration = 3600  # 1 hour cache
        self.fred_base_url = "https://api.stlouisfed.org/fred/series/observations"
        self.fred_api_key = st.secrets.get("fred_api", {}).get("key", "")
        
        # Metric configurations
        self.metrics_config = {
            'M2': {
                'fred_series': 'WM2NS',  # M2 Money Supply (weekly, not seasonally adjusted)
                'name': 'M2 Money Supply (Weekly)',
                'unit': 'Trillions USD',
                'green_threshold': 0.1,  # % week-over-week increase (more sensitive)
                'red_threshold': -0.1,  # % week-over-week decrease
            },
            'BANK_RESERVES': {
                'fred_series': 'WRESBAL',  # Total Reserves of Depository Institutions
                'name': 'Bank Reserve Balances',
                'unit': 'Billions USD',
                'green_threshold': 25,  # Billion USD week-over-week increase (more sensitive)
                'red_threshold': -25,  # Billion USD week-over-week decrease
            },
            'RRP': {
                'fred_series': 'RRPONTSYD',
                'name': 'Reverse Repo Usage',
                'unit': 'Billions USD',
                'green_threshold': 300,  # Below this is green
                'red_threshold': 800,  # Above this is red
            },
            'YIELD_10Y': {
                'fred_series': 'DGS10',
                'name': '10-Year Treasury Yield',
                'unit': 'Percent',
                'green_threshold': -0.1,  # Trending down
                'red_threshold': 0.1,  # Trending up
            },
            'YIELD_2Y': {
                'fred_series': 'DGS2',
                'name': '2-Year Treasury Yield',
                'unit': 'Percent',
                'green_threshold': -0.1,  # Trending down
                'red_threshold': 0.1,  # Trending up
            }
        }
    
    @st.cache_data(ttl=3600)
    def fetch_fred_data(_self, series_id: str, limit: int = 50) -> pd.DataFrame:
        """Fetch data from FRED API"""
        if not _self.fred_api_key:
            st.warning("FRED API key not configured. Using mock data.")
            return _self._get_mock_fred_data(series_id, limit)
        
        try:
            params = {
                'series_id': series_id,
                'api_key': _self.fred_api_key,
                'file_type': 'json',
                'limit': limit,
                'sort_order': 'desc'  # Get most recent data first
            }
            
            response = requests.get(_self.fred_base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            observations = data.get('observations', [])
            
            if not observations:
                return pd.DataFrame()
            
            df = pd.DataFrame(observations)
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df = df.dropna(subset=['value'])
            
            # Sort by date ascending for calculations (oldest to newest)
            df = df.sort_values('date').reset_index(drop=True)
            
            return df
            
        except Exception as e:
            st.warning(f"Failed to fetch FRED data for {series_id}: {e}")
            return _self._get_mock_fred_data(series_id, limit)

    @st.cache_data(ttl=3600) 
    def fetch_latest_fred_observation(_self, series_id: str) -> dict:
        """Fetch only the latest observation from FRED API for efficiency"""
        if not _self.fred_api_key:
            return {}
        
        try:
            params = {
                'series_id': series_id,
                'api_key': _self.fred_api_key,
                'file_type': 'json',
                'limit': 1,
                'sort_order': 'desc'  # Get the most recent observation only
            }
            
            response = requests.get(_self.fred_base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            observations = data.get('observations', [])
            
            if observations:
                obs = observations[0]
                return {
                    'date': pd.to_datetime(obs['date']),
                    'value': float(obs['value']) if obs['value'] != '.' else None
                }
            
            return {}
            
        except Exception as e:
            st.warning(f"Failed to fetch latest FRED observation for {series_id}: {e}")
            return {}
    
    def _get_mock_fred_data(self, series_id: str, limit: int) -> pd.DataFrame:
        """Generate mock data for demonstration when FRED API is not available"""
        dates = pd.date_range(end=datetime.now(), periods=limit, freq='D')
        
        # Generate realistic mock data based on series
        if series_id in ['M2SL', 'WM2NS']:  # Support both monthly and weekly M2 series
            base_value = 21000  # ~21T USD
            values = base_value + np.cumsum(np.random.normal(20, 50, limit))
        elif series_id in ['TOTRESNS', 'WRESBAL']:  # Support both old and new series IDs
            base_value = 3200  # ~3.2T USD
            values = base_value + np.cumsum(np.random.normal(0, 100, limit))
        elif series_id == 'RRPONTSYD':
            base_value = 500  # ~500B USD
            values = base_value + np.cumsum(np.random.normal(-5, 50, limit))
            values = np.clip(values, 0, 2000)  # Keep realistic bounds
        elif series_id in ['DGS10', 'DGS2']:
            base_value = 4.5 if series_id == 'DGS10' else 4.0
            values = base_value + np.cumsum(np.random.normal(0, 0.1, limit))
            values = np.clip(values, 0, 10)  # Keep realistic bounds
        else:
            values = np.random.normal(100, 10, limit)
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    @st.cache_data(ttl=3600)
    def fetch_crypto_metrics(_self) -> Dict[str, float]:
        """Fetch crypto-related liquidity metrics"""
        try:
            # Get stablecoin market cap from CoinGecko with retry logic
            stablecoin_url = "https://api.coingecko.com/api/v3/coins/markets"
            stablecoin_params = {
                'vs_currency': 'usd',
                'ids': 'tether,usd-coin,binance-usd,dai',
                'order': 'market_cap_desc',
                'per_page': 10,
                'page': 1
            }
            
            # Retry logic for rate limits with longer backoff
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    stablecoin_response = requests.get(stablecoin_url, params=stablecoin_params, timeout=10)
                    if stablecoin_response.status_code == 429:  # Too Many Requests
                        if attempt < max_retries - 1:
                            wait_time = 5 * (2 ** attempt)  # Exponential backoff starting at 5s
                            print(f"⚠️ CoinGecko rate limited, waiting {wait_time} seconds before retry...")
                            time.sleep(wait_time)
                            continue
                        else:
                            # Last attempt failed, raise to trigger fallback
                            stablecoin_response.raise_for_status()
                    stablecoin_response.raise_for_status()  # Raise exception for bad status codes
                    break  # Success, exit retry loop
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429 and attempt < max_retries - 1:
                        wait_time = 5 * (2 ** attempt)  # Exponential backoff starting at 5s
                        print(f"⚠️ CoinGecko rate limited, waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise  # Re-raise if not rate limit or last attempt
            stablecoin_data = stablecoin_response.json()
            
            # Validate response is a list
            if not isinstance(stablecoin_data, list):
                raise ValueError(f"Unexpected stablecoin API response format: {type(stablecoin_data)}")
            
            total_stablecoin_cap = sum(coin.get('market_cap', 0) for coin in stablecoin_data if isinstance(coin, dict))
            
            # Get DeFi TVL from DeFiLlama
            defi_url = "https://api.llama.fi/protocols"
            defi_response = requests.get(defi_url, timeout=10)
            defi_response.raise_for_status()
            defi_data = defi_response.json()
            
            # Validate response is a list
            if not isinstance(defi_data, list):
                raise ValueError(f"Unexpected DeFi API response format: {type(defi_data)}")
            
            total_defi_tvl = sum(protocol.get('tvl', 0) for protocol in defi_data[:50] if isinstance(protocol, dict))
            
            return {
                'stablecoin_mcap': total_stablecoin_cap / 1e9,  # Convert to billions
                'defi_tvl': total_defi_tvl / 1e9,  # Convert to billions
                'btc_dominance': 50.0,  # Mock data - would need additional API
                'total_crypto_mcap': 2500.0  # Mock data - would need additional API
            }
            
        except Exception as e:
            st.warning(f"Failed to fetch crypto metrics: {e}")
            return {
                'stablecoin_mcap': 125.0,  # Mock: ~125B USD
                'defi_tvl': 45.0,  # Mock: ~45B USD
                'btc_dominance': 50.0,
                'total_crypto_mcap': 2500.0
            }
    
    def calculate_metric_status(self, series_id: str, current_value: float, historical_data: pd.DataFrame) -> Tuple[str, float]:
        """Calculate traffic light status for a metric"""
        config = self.metrics_config.get(series_id, {})
        
        if len(historical_data) < 2:
            return 'amber', 0.0
        
        # Calculate change based on metric type
        if series_id == 'M2':
            # Week-over-week change for M2 (more responsive than monthly)
            if len(historical_data) >= 7:
                prev_value = historical_data.iloc[-7]['value']
                # Convert to scalar if needed
                if hasattr(prev_value, 'item'):
                    prev_value = prev_value.item()
                change = ((current_value - prev_value) / prev_value) * 100
            else:
                prev_value = historical_data.iloc[-2]['value']
                # Convert to scalar if needed
                if hasattr(prev_value, 'item'):
                    prev_value = prev_value.item()
                change = ((current_value - prev_value) / prev_value) * 100
            
            # Convert change to scalar if needed
            try:
                if hasattr(change, 'item'):
                    change = change.item()
                elif hasattr(change, 'iloc'):
                    change = change.iloc[0]
                elif hasattr(change, 'total_seconds'):  # timedelta object
                    change = change.total_seconds
                elif hasattr(change, 'dt') and hasattr(change.dt, 'total_seconds'):  # timedelta series
                    change = change.dt.total_seconds().iloc[0]
                else:
                    change = float(change)  # type: ignore
            except (ValueError, TypeError, AttributeError):
                change = 0.0
            
            # Ensure change is now a float
            try:
                change = float(change) if not isinstance(change, float) else change  # type: ignore
            except (ValueError, TypeError):
                change = 0.0
            
            if change >= config['green_threshold']:
                return 'green', change
            elif change <= config['red_threshold']:
                return 'red', change
            else:
                return 'amber', change
                
        elif series_id == 'BANK_RESERVES':
            # Week-over-week absolute change (more responsive than monthly)
            if len(historical_data) >= 7:
                prev_value = historical_data.iloc[-7]['value']
                # Convert to scalar if needed
                if hasattr(prev_value, 'item'):
                    prev_value = prev_value.item()
                change = current_value - prev_value
            else:
                prev_value = historical_data.iloc[-2]['value']
                # Convert to scalar if needed
                if hasattr(prev_value, 'item'):
                    prev_value = prev_value.item()
                change = current_value - prev_value
            
            # Convert change to scalar if needed
            try:
                if hasattr(change, 'item'):
                    change = change.item()
                elif hasattr(change, 'iloc'):
                    change = change.iloc[0]  # type: ignore
                else:
                    change = float(change)  # type: ignore
            except (ValueError, TypeError, AttributeError):
                change = 0.0
            
            if change >= config['green_threshold']:
                return 'green', change
            elif change <= config['red_threshold']:
                return 'red', change
            else:
                return 'amber', change
                
        elif series_id == 'RRP':
            # Current level thresholds
            if current_value < config['green_threshold']:
                return 'green', current_value
            elif current_value > config['red_threshold']:
                return 'red', current_value
            else:
                return 'amber', current_value
                
        elif series_id in ['YIELD_10Y', 'YIELD_2Y']:
            # 4-week trend
            if len(historical_data) >= 28:
                recent_data = historical_data.tail(28)
                trend = np.polyfit(range(len(recent_data)), recent_data['value'], 1)[0]
                
                if trend <= config['green_threshold']:
                    return 'green', trend
                elif trend >= config['red_threshold']:
                    return 'red', trend
                else:
                    return 'amber', trend
            else:
                return 'amber', 0.0
        
        return 'amber', 0.0
    
    def get_all_metrics(self) -> Dict[str, LiquidityMetric]:
        """Fetch and calculate all liquidity metrics"""
        metrics = {}
        fetch_time = datetime.now()  # When we retrieved the data
        
        # Fetch FRED metrics
        for metric_key, config in self.metrics_config.items():
            try:
                # Get latest observation for display
                latest_obs = self.fetch_latest_fred_observation(config['fred_series'])
                
                if latest_obs and latest_obs.get('value') is not None:
                    current_value = latest_obs['value']
                    observation_date = latest_obs['date']
                    
                    # Get historical data for trend calculation
                    historical_data = self.fetch_fred_data(config['fred_series'])
                    status, change = self.calculate_metric_status(metric_key, current_value, historical_data)
                    
                    # Convert units for display
                    if config['unit'] == 'Trillions USD':
                        display_value = current_value / 1000
                    elif config['unit'] == 'Billions USD':
                        display_value = current_value
                    else:
                        display_value = current_value
                    
                    metrics[metric_key] = LiquidityMetric(
                        name=config['name'],
                        label=metric_key,  # Use the metric key as label
                        value=display_value,
                        change=change,
                        status=status,
                        last_updated=observation_date,  # Actual data observation date from FRED
                        fetched_at=fetch_time,  # When we retrieved it
                        source='FRED',
                        unit=config['unit']
                    )
                else:
                    # Fallback to historical data method
                    data = self.fetch_fred_data(config['fred_series'])
                    
                    if not data.empty:
                        # Helper function to extract scalar values from pandas objects
                        def to_scalar(value):
                            try:
                                if hasattr(value, 'item'):
                                    return value.item()
                                elif hasattr(value, 'iloc') and len(value) == 1:
                                    return value.iloc[0]
                                elif hasattr(value, 'values') and len(value.values) == 1:
                                    return value.values[0]
                                elif hasattr(value, 'total_seconds'):  # timedelta
                                    return value.total_seconds()
                                else:
                                    return float(value)
                            except (ValueError, TypeError, AttributeError):
                                return 0.0  # fallback value
                        
                        current_value = to_scalar(data.iloc[-1]['value'])
                        status, change = self.calculate_metric_status(metric_key, float(current_value), data)
                        
                        # Convert units for display
                        if config['unit'] == 'Trillions USD':
                            display_value = current_value / 1000
                        elif config['unit'] == 'Billions USD':
                            display_value = current_value
                        else:
                            display_value = current_value
                        
                        display_value = to_scalar(display_value)
                        
                        # Get the last updated date as scalar
                        last_updated_raw = data.iloc[-1]['date']
                        try:
                            if hasattr(last_updated_raw, 'to_pydatetime'):
                                last_updated = last_updated_raw.to_pydatetime()
                            elif hasattr(last_updated_raw, 'item'):
                                last_updated = last_updated_raw.item()
                            else:
                                last_updated = last_updated_raw
                            
                            # If it's still not a datetime, use fetch_time as fallback
                            if not isinstance(last_updated, datetime):
                                last_updated = fetch_time
                        except (ValueError, TypeError, AttributeError):
                            last_updated = fetch_time  # type: ignore
                        
                        metrics[metric_key] = LiquidityMetric(
                            name=config['name'],
                            label=metric_key,  # Use the metric key as label
                            value=float(display_value),
                            change=change,
                            status=status,
                            last_updated=last_updated,  # Actual data observation date
                            fetched_at=fetch_time,  # When we retrieved it
                            source='FRED',
                            unit=config['unit']
                        )
                    
            except Exception as e:
                st.warning(f"Failed to process {metric_key}: {e}")
        
        # Fetch crypto metrics
        try:
            crypto_data = self.fetch_crypto_metrics()
            
            # Stablecoin supply metric
            metrics['STABLECOIN'] = LiquidityMetric(
                name='Stablecoin Market Cap',
                label='STABLECOIN',
                value=crypto_data['stablecoin_mcap'],
                change=2.1,  # Mock change - would calculate from historical data
                status='green',  # Mock status - would calculate properly
                last_updated=fetch_time,  # Real-time data, so observation = fetch time
                fetched_at=fetch_time,
                source='CoinGecko',
                unit='Billions USD'
            )
            
            # DeFi TVL metric
            metrics['DEFI_TVL'] = LiquidityMetric(
                name='DeFi Total Value Locked',
                label='DEFI_TVL',
                value=crypto_data['defi_tvl'],
                change=5.8,  # Mock change
                status='green',  # Mock status
                last_updated=fetch_time,  # Real-time data, so observation = fetch time
                fetched_at=fetch_time,
                source='DeFiLlama',
                unit='Billions USD'
            )
            
        except Exception as e:
            st.warning(f"Failed to process crypto metrics: {e}")
        
        return metrics
    
    def calculate_overall_liquidity_score(self, metrics: Dict[str, LiquidityMetric]) -> Tuple[str, int]:
        """Calculate overall liquidity health score"""
        status_weights = {'green': 1, 'amber': 0, 'red': -1}
        
        total_score = 0
        total_metrics = len(metrics)
        
        for metric in metrics.values():
            total_score += status_weights.get(metric.status, 0)
        
        # Convert to 0-100 scale
        normalized_score = int(((total_score + total_metrics) / (2 * total_metrics)) * 100)
        
        # Determine overall status
        if normalized_score >= 70:
            overall_status = 'green'
        elif normalized_score >= 40:
            overall_status = 'amber'
        else:
            overall_status = 'red'
        
        return overall_status, normalized_score

def format_metric_value(value: float, unit: str) -> str:
    """Format metric values for display"""
    if 'Billions' in unit or 'Trillions' in unit:
        if value >= 1000:
            return f"${value/1000:.1f}T"
        else:
            return f"${value:.1f}B"
    elif 'Percent' in unit:
        return f"{value:.2f}%"
    else:
        return f"{value:.2f}"

def get_status_color(status: str) -> str:
    """Get color for status indicators"""
    colors = {
        'green': '#28a745',
        'amber': '#ffc107', 
        'red': '#dc3545'
    }
    return colors.get(status, '#6c757d')

def get_status_emoji(status: str) -> str:
    """Get emoji for status indicators"""
    emojis = {
        'green': '🟢',
        'amber': '🟡',
        'red': '🔴'
    }
    return emojis.get(status, '⚪')

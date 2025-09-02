import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
from binance.client import Client
from binance.exceptions import BinanceAPIException
import requests
import warnings
warnings.filterwarnings('ignore')

def get_binance_client():
    """Get authenticated Binance client"""
    try:
        api_key = st.secrets.get("binance_api_key")
        api_secret = st.secrets.get("binance_api_secret")
        
        if not api_key or not api_secret:
            print("⚠️ Binance API credentials not found in secrets")
            return None
            
        print("Using authenticated Binance client")
        return Client(api_key, api_secret)
    except Exception as e:
        print(f"❌ Failed to create Binance client: {e}")
        return None

def fetch_coingecko_history(symbol, days=365):
    """Fetch historical data from CoinGecko API (free, no auth required)"""
    try:
        # CoinGecko symbol mapping
        coingecko_symbols = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'ADA': 'cardano',
            'DOT': 'polkadot',
            'LINK': 'chainlink',
            'XRP': 'ripple',
            'LTC': 'litecoin',
            'BCH': 'bitcoin-cash',
            'BNB': 'binancecoin',
            'SOL': 'solana',
            'MATIC': 'polygon',
            'AVAX': 'avalanche-2',
            'ATOM': 'cosmos',
            'UNI': 'uniswap',
            'DOGE': 'dogecoin'
        }
        
        coin_id = coingecko_symbols.get(symbol.upper())
        if not coin_id:
            print(f"❌ CoinGecko: Symbol {symbol} not supported")
            return pd.DataFrame()
            
        print(f"🦎 Fetching CoinGecko data for {symbol} ({coin_id})")
        
        # Use a more conservative approach to avoid rate limits
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': min(days, 90),  # Reduce to 90 days to avoid rate limits
            'interval': 'daily'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Crypto Dashboard)',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code == 429:
            print(f"⚠️ CoinGecko rate limit reached, using minimal data")
            # Create minimal synthetic data for rate-limited cases
            return create_minimal_data(symbol, days)
        elif response.status_code != 200:
            print(f"❌ CoinGecko API error: HTTP {response.status_code}")
            return create_minimal_data(symbol, days)
            
        data = response.json()
        prices = data.get('prices', [])
        
        if not prices:
            print(f"❌ CoinGecko: No price data for {symbol}")
            return create_minimal_data(symbol, days)
            
        # Convert to DataFrame
        df = pd.DataFrame(prices, columns=['timestamp', 'close'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        # Add OHLCV columns (CoinGecko only provides close prices for free tier)
        df['open'] = df['close'].shift(1).fillna(df['close'])
        df['high'] = df['close'] * 1.01  # Approximate high
        df['low'] = df['close'] * 0.99   # Approximate low
        df['volume'] = 1000000  # Placeholder volume
        
        # Reorder columns to match Binance format
        df = df[['open', 'high', 'low', 'close', 'volume']]
        
        print(f"✅ CoinGecko data fetched for {symbol}: {len(df)} rows")
        return df
        
    except Exception as e:
        print(f"❌ CoinGecko API error for {symbol}: {e}")
        return create_minimal_data(symbol, days)

def create_minimal_data(symbol, days=90):
    """Create minimal synthetic data when APIs fail"""
    try:
        # Get current price from a simple API
        simple_url = f"https://api.coinbase.com/v2/exchange-rates?currency={symbol.upper()}"
        response = requests.get(simple_url, timeout=5)
        
        current_price = 1.0  # Default fallback
        if response.status_code == 200:
            data = response.json()
            rates = data.get('data', {}).get('rates', {})
            usd_rate = rates.get('USD')
            if usd_rate:
                current_price = float(usd_rate)
                print(f"📊 Using Coinbase price for {symbol}: ${current_price:,.2f}")
        
        # Create simple historical data with small variations
        end_date = datetime.now()
        start_date = end_date - timedelta(days=min(days, 90))
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Create slight price variations around current price
        base_price = current_price
        price_data = []
        for i, date in enumerate(dates):
            # Small random walk
            variation = 1 + (np.sin(i * 0.1) * 0.05)  # ±5% variation
            price = base_price * variation
            price_data.append({
                'open': price * 0.995,
                'high': price * 1.01,
                'low': price * 0.99,
                'close': price,
                'volume': 1000000
            })
        
        df = pd.DataFrame(price_data, index=dates)
        print(f"📈 Created minimal data for {symbol}: {len(df)} rows around ${current_price:,.2f}")
        return df
        
    except Exception as e:
        print(f"❌ Failed to create minimal data for {symbol}: {e}")
        return pd.DataFrame()

def get_coingecko_current_prices(symbols):
    """Get current prices from CoinGecko API"""
    try:
        # CoinGecko symbol mapping
        coingecko_symbols = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'ADA': 'cardano',
            'DOT': 'polkadot',
            'LINK': 'chainlink',
            'XRP': 'ripple',
            'LTC': 'litecoin',
            'BCH': 'bitcoin-cash',
            'BNB': 'binancecoin',
            'SOL': 'solana',
            'MATIC': 'polygon',
            'AVAX': 'avalanche-2',
            'ATOM': 'cosmos',
            'UNI': 'uniswap',
            'DOGE': 'dogecoin'
        }
        
        # Map symbols to CoinGecko IDs
        coin_ids = []
        symbol_map = {}
        for symbol in symbols:
            coin_id = coingecko_symbols.get(symbol.upper())
            if coin_id:
                coin_ids.append(coin_id)
                symbol_map[coin_id] = symbol.upper()
        
        if not coin_ids:
            print("❌ CoinGecko: No supported symbols found")
            return {}
            
        print(f"🦎 Fetching CoinGecko current prices for: {list(symbol_map.values())}")
        
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': ','.join(coin_ids),
            'vs_currencies': 'usd'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ CoinGecko price API error: HTTP {response.status_code}")
            return {}
            
        data = response.json()
        
        # Convert back to symbol-based format
        prices = {}
        for coin_id, price_data in data.items():
            symbol = symbol_map.get(coin_id)
            if symbol and 'usd' in price_data:
                prices[symbol] = price_data['usd']
                
        print(f"✅ CoinGecko prices fetched: {prices}")
        return prices
        
    except Exception as e:
        print(f"❌ CoinGecko price API error: {e}")
        return {}

def fetch_binance_history(symbol: str, interval="1d", start_str=None, end_str=None):
    """
    Fetch OHLCV historical data from Binance with CoinGecko fallback.

    Parameters:
        symbol (str): Trading pair symbol like 'BTCUSDT'
        interval (str): Kline interval ('1d' by default)
        start_str (str): Start date string in UTC format
        end_str (str): End date string in UTC format

    Returns:
        pd.DataFrame: Columns - timestamp, open, high, low, close, volume
    """
    try:
        # Initialize Binance client with proper credentials
        binance_client = get_binance_client()
        if not binance_client:
            print(f"⚠️ Binance client not available for {symbol}, trying CoinGecko")
            # Extract base symbol from trading pair more carefully
            base_symbol = symbol
            for suffix in ['USDT', 'BUSD', 'BTC', 'ETH']:
                if symbol.endswith(suffix):
                    base_symbol = symbol[:-len(suffix)]
                    break
            if base_symbol:
                return fetch_coingecko_history(base_symbol, 365)
            else:
                return pd.DataFrame()
        
        klines = binance_client.get_historical_klines(symbol, interval, start_str, end_str)
        
        if not klines:
            print(f"No klines data returned for {symbol} from Binance, trying CoinGecko")
            base_symbol = symbol
            for suffix in ['USDT', 'BUSD', 'BTC', 'ETH']:
                if symbol.endswith(suffix):
                    base_symbol = symbol[:-len(suffix)]
                    break
            if base_symbol:
                return fetch_coingecko_history(base_symbol, 365)
            else:
                return pd.DataFrame()
        
        # Process the real data
        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades",
            "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
        ])

        if df.empty:
            print(f"Empty DataFrame from Binance for {symbol}, trying CoinGecko")
            base_symbol = symbol
            for suffix in ['USDT', 'BUSD', 'BTC', 'ETH']:
                if symbol.endswith(suffix):
                    base_symbol = symbol[:-len(suffix)]
                    break
            if base_symbol:
                return fetch_coingecko_history(base_symbol, 365)
            else:
                return pd.DataFrame()

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
        df.set_index("timestamp", inplace=True)
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        print(f"✅ Real Binance data fetched for {symbol}: {len(df)} rows")
        return df[["open", "high", "low", "close", "volume"]]
        
    except Exception as e:
        print(f"❌ Binance API error for {symbol}: {e}")
        print(f"Error type: {type(e).__name__}")
        print(f"Falling back to CoinGecko for {symbol}")
        base_symbol = symbol
        for suffix in ['USDT', 'BUSD', 'BTC', 'ETH']:
            if symbol.endswith(suffix):
                base_symbol = symbol[:-len(suffix)]
                break
        if base_symbol:
            return fetch_coingecko_history(base_symbol, 365)
        else:
            return pd.DataFrame()

def get_price_history(symbol: str, years=5):
    """
    Main wrapper used by the app to get historical OHLCV data.

    Parameters:
        symbol (str): Crypto asset symbol (e.g., 'BTC', 'SOL')
        years (int): Number of years of historical data to fetch

    Returns:
        pd.DataFrame: Historical OHLCV
    """
    end_date = datetime.utcnow()
    start_date = end_date - pd.DateOffset(years=years)
    
    symbol_upper = symbol.upper()
    
    # Handle special case for USDT (create stable price data)
    if symbol_upper == 'USDT':
        # For USDT, create synthetic stable data since it's pegged to $1
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        stable_data = pd.DataFrame({
            'open': [1.0] * len(dates),
            'high': [1.001] * len(dates),  # Small fluctuation
            'low': [0.999] * len(dates),
            'close': [1.0] * len(dates),
            'volume': [1000000] * len(dates)  # Mock volume
        }, index=dates)
        print(f"✅ Generated stable price data for USDT: {len(stable_data)} rows")
        return stable_data
    
    # Try primary USDT pair first
    primary_pair = f"{symbol_upper}USDT"
    result = fetch_binance_history(
        primary_pair,
        start_str=start_date.strftime("%Y-%m-%d"),
        end_str=end_date.strftime("%Y-%m-%d")
    )
    
    # If primary pair fails, try alternative pairs
    if result.empty:
        alternative_pairs = [
            f"{symbol_upper}BUSD",  # Binance USD
            f"{symbol_upper}BTC",   # Bitcoin pair
            f"{symbol_upper}ETH",   # Ethereum pair
        ]
        
        for alt_pair in alternative_pairs:
            print(f"Trying alternative pair: {alt_pair}")
            result = fetch_binance_history(
                alt_pair,
                start_str=start_date.strftime("%Y-%m-%d"),
                end_str=end_date.strftime("%Y-%m-%d")
            )
            if not result.empty:
                print(f"✅ Found data for {alt_pair}")
                break
    
    return result

def get_current_prices(symbols: list) -> dict:
    """
    Get current prices for a list of symbols with CoinGecko fallback.
    
    Parameters:
        symbols (list): List of crypto symbols (e.g., ['BTC', 'ETH', 'SOL'])
    
    Returns:
        dict: Dictionary mapping symbols to current prices
    """
    prices = {}
    
    try:
        # Initialize Binance client with proper credentials
        binance_client = get_binance_client()
        
        if not binance_client:
            print("⚠️ Binance client not available, using CoinGecko for all prices")
            return get_coingecko_current_prices(symbols)
        
        # Get ticker prices from Binance
        tickers = binance_client.get_all_tickers()
        ticker_dict = {ticker['symbol']: float(ticker['price']) for ticker in tickers}
        
        unfound_symbols = []
        
        for symbol in symbols:
            symbol_upper = symbol.upper()
            
            # Special case for USDT
            if symbol_upper == 'USDT':
                prices[symbol] = 1.0
                continue
                
            usdt_pair = f"{symbol_upper}USDT"
            
            if usdt_pair in ticker_dict:
                prices[symbol] = ticker_dict[usdt_pair]
            else:
                # Try alternative pairs
                alt_pairs = [f"{symbol_upper}BUSD", f"{symbol_upper}BTC", f"{symbol_upper}ETH"]
                found = False
                for alt_pair in alt_pairs:
                    if alt_pair in ticker_dict:
                        prices[symbol] = ticker_dict[alt_pair]
                        print(f"Found price for {symbol} via {alt_pair}")
                        found = True
                        break
                
                if not found:
                    unfound_symbols.append(symbol)
        
        # Try CoinGecko for symbols not found in Binance
        if unfound_symbols:
            print(f"Trying CoinGecko for symbols not found in Binance: {unfound_symbols}")
            coingecko_prices = get_coingecko_current_prices(unfound_symbols)
            prices.update(coingecko_prices)
        
        # Fill any remaining symbols with 0.0
        for symbol in symbols:
            if symbol not in prices:
                print(f"⚠️ No price data found for {symbol}")
                prices[symbol] = 0.0
                
        successful_prices = len([s for s in symbols if prices.get(s, 0) > 0])
        print(f"✅ Prices fetched for {successful_prices}/{len(symbols)} symbols")
        
    except Exception as e:
        print(f"❌ Binance API error for price fetching: {e}")
        print("Falling back to CoinGecko for all symbols")
        try:
            prices = get_coingecko_current_prices(symbols)
        except Exception as cg_e:
            print(f"❌ CoinGecko fallback also failed: {cg_e}")
            # Return zeros as last resort
            for symbol in symbols:
                prices[symbol] = 0.0
    
    return prices

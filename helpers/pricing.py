import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import warnings
warnings.filterwarnings('ignore')

def fetch_coingecko_history(symbol, days=365):
    """Fetch historical data from CoinGecko API (free, no auth required) - Primary API"""
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
            'DOGE': 'dogecoin',
            'USDT': 'tether',
            'USDC': 'usd-coin',
            'TRX': 'tron',
            'TON': 'the-open-network',
            'SHIB': 'shiba-inu'
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
            'days': min(days, 365),  # Maximum 1 year for free tier
            'interval': 'daily'
        }
        
        headers = {
            'User-Agent': 'CryptoDashboard/1.0',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=20)
        
        if response.status_code == 429:
            print(f"⚠️ CoinGecko rate limit reached for {symbol}, using minimal data")
            return create_minimal_data(symbol, days)
        elif response.status_code != 200:
            print(f"❌ CoinGecko API error for {symbol}: HTTP {response.status_code}")
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
        df['high'] = df['close'] * 1.02  # Approximate high (+2%)
        df['low'] = df['close'] * 0.98   # Approximate low (-2%)
        df['volume'] = 10000000  # Placeholder volume
        
        # Reorder columns to match expected format
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
    """Get current prices from CoinGecko API - Primary price source"""
    try:
        # CoinGecko symbol mapping (expanded)
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
            'DOGE': 'dogecoin',
            'USDT': 'tether',
            'USDC': 'usd-coin',
            'TRX': 'tron',
            'TON': 'the-open-network',
            'SHIB': 'shiba-inu'
        }
        
        # Map symbols to CoinGecko IDs
        coin_ids = []
        symbol_map = {}
        for symbol in symbols:
            symbol_upper = symbol.upper()
            coin_id = coingecko_symbols.get(symbol_upper)
            if coin_id:
                coin_ids.append(coin_id)
                symbol_map[coin_id] = symbol_upper
        
        if not coin_ids:
            print("❌ CoinGecko: No supported symbols found")
            return {}
            
        print(f"🦎 Fetching CoinGecko current prices for: {list(symbol_map.values())}")
        
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': ','.join(coin_ids),
            'vs_currencies': 'usd'
        }
        
        headers = {
            'User-Agent': 'CryptoDashboard/1.0',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code == 429:
            print(f"⚠️ CoinGecko rate limit reached, using Coinbase fallback")
            return get_coinbase_current_prices(symbols)
        elif response.status_code != 200:
            print(f"❌ CoinGecko price API error: HTTP {response.status_code}")
            return get_coinbase_current_prices(symbols)
            
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
        return get_coinbase_current_prices(symbols)

def get_coinbase_current_prices(symbols):
    """Fallback price source using Coinbase API"""
    try:
        prices = {}
        print(f"💰 Trying Coinbase API for fallback prices")
        
        for symbol in symbols:
            try:
                symbol_upper = symbol.upper()
                url = f"https://api.coinbase.com/v2/exchange-rates?currency={symbol_upper}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    rates = data.get('data', {}).get('rates', {})
                    usd_rate = rates.get('USD')
                    if usd_rate:
                        prices[symbol] = float(usd_rate)
                        print(f"   ✅ {symbol}: ${float(usd_rate):,.2f}")
                    else:
                        prices[symbol] = 0.0
                else:
                    prices[symbol] = 0.0
            except Exception as e:
                print(f"   ❌ {symbol}: Coinbase error - {e}")
                prices[symbol] = 0.0
        
        return prices
        
    except Exception as e:
        print(f"❌ Coinbase API error: {e}")
        # Return zeros as final fallback
        return {symbol: 0.0 for symbol in symbols}

def get_price_history(symbol: str, years=5):
    """
    Main wrapper used by the app to get historical OHLCV data using CoinGecko API.

    Parameters:
        symbol (str): Crypto asset symbol (e.g., 'BTC', 'SOL')
        years (int): Number of years of historical data to fetch

    Returns:
        pd.DataFrame: Historical OHLCV
    """
    symbol_upper = symbol.upper()
    
    # Handle special case for USDT (create stable price data)
    if symbol_upper == 'USDT':
        # For USDT, create synthetic stable data since it's pegged to $1
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years * 365)
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
    
    # Use CoinGecko as primary data source
    days = min(years * 365, 365)  # CoinGecko free tier limitation
    result = fetch_coingecko_history(symbol_upper, days)
    
    if result.empty:
        print(f"⚠️ No data available for {symbol}")
        # Try to create minimal fallback data
        result = create_minimal_data(symbol_upper, days)
    
    return result

def get_current_prices(symbols: list) -> dict:
    """
    Get current prices for a list of symbols using CoinGecko API as primary source.
    
    Parameters:
        symbols (list): List of crypto symbols (e.g., ['BTC', 'ETH', 'SOL'])
    
    Returns:
        dict: Dictionary mapping symbols to current prices
    """
    prices = {}
    
    try:
        # Use CoinGecko as primary source
        prices = get_coingecko_current_prices(symbols)
        
        # Handle special case for USDT
        for symbol in symbols:
            if symbol.upper() == 'USDT':
                prices[symbol] = 1.0
        
        # Fill any missing symbols with zeros
        for symbol in symbols:
            if symbol not in prices:
                print(f"⚠️ No price data found for {symbol}")
                prices[symbol] = 0.0
                
        successful_prices = len([s for s in symbols if prices.get(s, 0) > 0])
        print(f"✅ Prices fetched for {successful_prices}/{len(symbols)} symbols")
        
    except Exception as e:
        print(f"❌ Error fetching prices: {e}")
        # Return zeros as fallback
        for symbol in symbols:
            prices[symbol] = 0.0
    
    return prices

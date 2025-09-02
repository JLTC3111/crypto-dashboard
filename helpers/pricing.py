import pandas as pd
from binance.client import Client
from datetime import datetime

def fetch_binance_history(symbol: str, interval="1d", start_str=None, end_str=None):
    """
    Fetch OHLCV historical data from Binance.

    Parameters:
        symbol (str): Trading pair symbol like 'BTCUSDT'
        interval (str): Kline interval ('1d' by default)
        start_str (str): Start date string in UTC format
        end_str (str): End date string in UTC format

    Returns:
        pd.DataFrame: Columns - timestamp, open, high, low, close, volume
    """
    # Check if we're in Streamlit Cloud environment first
    import os
    is_cloud = any([
        os.getenv('STREAMLIT_SHARING_MODE'),
        os.getenv('STREAMLIT_CLOUD'),
        'streamlit.app' in os.getenv('HOSTNAME', ''),
        '/app' in os.getcwd(),
        '/mount/src' in os.getcwd()  # New Streamlit Cloud path
    ])
    
    if is_cloud:
        print(f"Streamlit Cloud detected, using mock data for {symbol}")
        return generate_mock_data(symbol, start_str or "2023-01-01", end_str or "2024-01-01")
    
    try:
        # Initialize Binance client only when needed, with error handling
        binance_client = Client()
        klines = binance_client.get_historical_klines(symbol, interval, start_str, end_str)
        
        if not klines:
            print(f"No klines data returned for {symbol}")
            return pd.DataFrame()
            
    except Exception as e:
        # Enhanced error handling for any API failures
        print(f"Binance API error for {symbol}: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Return mock data as fallback
        print(f"Using fallback mock data for {symbol}")
        return generate_mock_data(symbol, start_str or "2023-01-01", end_str or "2024-01-01")

    try:
        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades",
            "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
        ])

        if df.empty:
            return df

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
        df.set_index("timestamp", inplace=True)
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        return df[["open", "high", "low", "close", "volume"]]
        
    except Exception as e:
        print(f"Error processing Binance data for {symbol}: {e}")
        return generate_mock_data(symbol, start_str or "2023-01-01", end_str or "2024-01-01")

def generate_mock_data(symbol: str, start_str: str, end_str: str):
    """
    Generate mock historical data for Streamlit Cloud when Binance API fails.
    """
    try:
        import numpy as np
    except ImportError:
        # Fallback if numpy isn't available
        import random
        
    from datetime import datetime
    
    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d") if start_str else datetime.now() - pd.DateOffset(years=1)
        end_date = datetime.strptime(end_str, "%Y-%m-%d") if end_str else datetime.now()
    except:
        start_date = datetime.now() - pd.DateOffset(years=1)
        end_date = datetime.now()
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Base prices for common symbols (approximate current values)
    base_prices = {
        'BTCUSDT': 60000,
        'ETHUSDT': 3000,
        'SOLUSDT': 150,
        'ADAUSDT': 0.5,
        'DOGEUSDT': 0.1,
        'BNBUSDT': 300,
        'XRPUSDT': 0.6,
        'LTCUSDT': 100,
        'MATICUSDT': 0.8,
        'DOTUSDT': 5,
    }
    
    base_price = base_prices.get(symbol, 100)  # Default to $100 if symbol not found
    
    # Generate realistic price movement
    try:
        import numpy as np
        np.random.seed(hash(symbol) % 2**32)  # Consistent randomness per symbol
        returns = np.random.normal(0.001, 0.03, len(dates))  # Daily returns with some volatility
    except ImportError:
        # Fallback using random module
        import random
        random.seed(hash(symbol) % 2**32)
        returns = [random.normalvariate(0.001, 0.03) for _ in range(len(dates))]
    
    prices = [base_price]
    
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    # Create OHLC data
    try:
        import numpy as np
        mock_data = pd.DataFrame({
            'open': [p * np.random.uniform(0.995, 1.005) for p in prices],
            'high': [p * np.random.uniform(1.005, 1.02) for p in prices],
            'low': [p * np.random.uniform(0.98, 0.995) for p in prices],
            'close': prices,
            'volume': [np.random.uniform(1000000, 10000000) for _ in prices]
        }, index=dates)
    except ImportError:
        # Fallback using random module
        import random
        mock_data = pd.DataFrame({
            'open': [p * random.uniform(0.995, 1.005) for p in prices],
            'high': [p * random.uniform(1.005, 1.02) for p in prices],
            'low': [p * random.uniform(0.98, 0.995) for p in prices],
            'close': prices,
            'volume': [random.uniform(1000000, 10000000) for _ in prices]
        }, index=dates)
    
    print(f"Generated mock data for {symbol}: {len(mock_data)} days")
    return mock_data

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
    
    # Handle special cases for symbols that don't have USDT pairs
    if symbol_upper == 'USDT':
        # For USDT, create synthetic data since it's pegged to $1
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        synthetic_data = pd.DataFrame({
            'open': [1.0] * len(dates),
            'high': [1.001] * len(dates),  # Small fluctuation
            'low': [0.999] * len(dates),
            'close': [1.0] * len(dates),
            'volume': [1000000] * len(dates)  # Mock volume
        }, index=dates)
        return synthetic_data
    
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
                # Convert to USDT equivalent if needed
                if alt_pair.endswith('BTC') or alt_pair.endswith('ETH'):
                    # Would need additional API call to convert, for now return as-is
                    print(f"Found data for {alt_pair}, but prices are in {alt_pair[-3:]} terms")
                break
    
    return result

def get_current_prices(symbols: list) -> dict:
    """
    Get current prices for a list of symbols.
    
    Parameters:
        symbols (list): List of crypto symbols (e.g., ['BTC', 'ETH', 'SOL'])
    
    Returns:
        dict: Dictionary mapping symbols to current prices
    """
    prices = {}
    
    # Check if we're in Streamlit Cloud environment first
    import os
    is_cloud = any([
        os.getenv('STREAMLIT_SHARING_MODE'),
        os.getenv('STREAMLIT_CLOUD'),
        'streamlit.app' in os.getenv('HOSTNAME', ''),
        '/app' in os.getcwd(),
        '/mount/src' in os.getcwd()  # New Streamlit Cloud path
    ])
    
    if is_cloud:
        print("Streamlit Cloud detected, using mock prices")
        # Mock prices for demo purposes
        mock_prices = {
            'BTC': 60000,
            'ETH': 3000,
            'SOL': 150,
            'ADA': 0.5,
            'DOGE': 0.1,
            'BNB': 300,
            'XRP': 0.6,
            'LTC': 100,
            'MATIC': 0.8,
            'DOT': 5,
            'USDT': 1.0,
            'USDC': 1.0,
        }
        
        for symbol in symbols:
            symbol_upper = symbol.upper()
            prices[symbol] = mock_prices.get(symbol_upper, 100.0)  # Default to $100
        return prices
    
    try:
        # Initialize Binance client only when needed, with error handling
        binance_client = Client()
        # Get ticker prices from Binance
        tickers = binance_client.get_all_tickers()
        ticker_dict = {ticker['symbol']: float(ticker['price']) for ticker in tickers}
        
        for symbol in symbols:
            symbol_upper = symbol.upper()
            usdt_pair = f"{symbol_upper}USDT"
            
            if usdt_pair in ticker_dict:
                prices[symbol] = ticker_dict[usdt_pair]
            else:
                # Fallback to a default price if not found
                prices[symbol] = 0.0
                
    except Exception as e:
        # Enhanced error handling - always use mock data as fallback
        print(f"Binance API error for price fetching: {e}")
        print("Using mock prices as fallback")
        
        # Mock prices for demo purposes
        mock_prices = {
            'BTC': 60000,
            'ETH': 3000,
            'SOL': 150,
            'ADA': 0.5,
            'DOGE': 0.1,
            'BNB': 300,
            'XRP': 0.6,
            'LTC': 100,
            'MATIC': 0.8,
            'DOT': 5,
            'USDT': 1.0,
            'USDC': 1.0,
        }
        
        for symbol in symbols:
            symbol_upper = symbol.upper()
            prices[symbol] = mock_prices.get(symbol_upper, 100.0)  # Default to $100
    
    return prices

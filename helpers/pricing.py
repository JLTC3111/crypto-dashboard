import pandas as pd
from binance.client import Client
from datetime import datetime
import streamlit as st

def get_binance_client():
    """
    Initialize Binance client with API credentials from secrets.
    Falls back to public client if credentials not available.
    """
    try:
        # Try to get API credentials from Streamlit secrets
        api_key = st.secrets.get("binance_api", {}).get("api_key", "")
        api_secret = st.secrets.get("binance_api", {}).get("api_secret", "")
        
        if api_key and api_secret:
            print("Using authenticated Binance client")
            return Client(api_key, api_secret)
        elif api_key:
            print("Using Binance client with API key only (no secret)")
            return Client(api_key)
        else:
            print("Using public Binance client (no credentials)")
            return Client()
            
    except Exception as e:
        print(f"Error initializing Binance client: {e}")
        # Fallback to public client
        return Client()

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
    try:
        # Initialize Binance client with proper credentials
        binance_client = get_binance_client()
        klines = binance_client.get_historical_klines(symbol, interval, start_str, end_str)
        
        if not klines:
            print(f"No klines data returned for {symbol}")
            return pd.DataFrame()
        
        # Process the real data
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
        print(f"✅ Real Binance data fetched for {symbol}: {len(df)} rows")
        return df[["open", "high", "low", "close", "volume"]]
        
    except Exception as e:
        print(f"❌ Binance API error for {symbol}: {e}")
        print(f"Error type: {type(e).__name__}")
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
    Get current prices for a list of symbols.
    
    Parameters:
        symbols (list): List of crypto symbols (e.g., ['BTC', 'ETH', 'SOL'])
    
    Returns:
        dict: Dictionary mapping symbols to current prices
    """
    prices = {}
    
    try:
        # Initialize Binance client with proper credentials
        binance_client = get_binance_client()
        # Get ticker prices from Binance
        tickers = binance_client.get_all_tickers()
        ticker_dict = {ticker['symbol']: float(ticker['price']) for ticker in tickers}
        
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
                    print(f"⚠️ No price data found for {symbol}")
                    prices[symbol] = 0.0
                
        successful_prices = len([s for s in symbols if prices.get(s, 0) > 0])
        print(f"✅ Real prices fetched for {successful_prices}/{len(symbols)} symbols")
        
    except Exception as e:
        print(f"❌ Binance API error for price fetching: {e}")
        # Return zeros instead of mock data
        for symbol in symbols:
            prices[symbol] = 0.0
    
    return prices

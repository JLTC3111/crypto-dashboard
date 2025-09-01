import pandas as pd
from binance.client import Client
from datetime import datetime

# Initialize Binance client
binance_client = Client()

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
        klines = binance_client.get_historical_klines(symbol, interval, start_str, end_str)
    except Exception as e:
        # Return empty dataframe if symbol doesn't exist
        return pd.DataFrame()

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

    return fetch_binance_history(
        f"{symbol.upper()}USDT",
        start_str=start_date.strftime("%Y-%m-%d"),
        end_str=end_date.strftime("%Y-%m-%d")
    )

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
        # Return default prices if API fails
        for symbol in symbols:
            prices[symbol] = 0.0
    
    return prices

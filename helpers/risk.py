import numpy as np
import pandas as pd

def max_drawdown(prices):
    """
    Calculate maximum drawdown from a price series
    
    Args:
        prices: pandas Series or array-like of prices
    
    Returns:
        float: Maximum drawdown (negative value)
    """
    try:
        if prices is None or len(prices) == 0:
            return 0.0
        
        # Convert to pandas Series if needed
        if not isinstance(prices, pd.Series):
            prices = pd.Series(prices)
        
        # Remove any NaN values
        prices = prices.dropna()
        
        if len(prices) == 0:
            return 0.0
            
        peak = prices.cummax()
        dd = (prices - peak) / peak
        return float(dd.min()) if len(dd) > 0 else 0.0
    except Exception as e:
        print(f"Error calculating max drawdown: {e}")
        return 0.0

def sharpe_ratio(prices, risk_free_rate=0.01):
    """
    Calculate Sharpe ratio from a price series
    
    Args:
        prices: pandas Series or array-like of prices
        risk_free_rate: Annual risk-free rate (default 1%)
    
    Returns:
        float: Annualized Sharpe ratio
    """
    try:
        if prices is None or len(prices) < 2:
            return 0.0
        
        # Convert to pandas Series if needed
        if not isinstance(prices, pd.Series):
            prices = pd.Series(prices)
        
        # Calculate returns
        daily_returns = prices.pct_change().dropna()
        
        if len(daily_returns) == 0 or daily_returns.std() == 0:
            return 0.0
        
        # Calculate excess returns
        excess_returns = daily_returns - (risk_free_rate / 252)
        
        # Calculate Sharpe ratio (annualized)
        return float(excess_returns.mean() / excess_returns.std() * np.sqrt(252))
    except Exception as e:
        print(f"Error calculating Sharpe ratio: {e}")
        return 0.0

def value_at_risk(prices, confidence=0.95):
    """
    Calculate Value at Risk (VaR) from a price series
    
    Args:
        prices: pandas Series or array-like of prices
        confidence: Confidence level (default 95%)
    
    Returns:
        float: VaR at specified confidence level
    """
    try:
        if prices is None or len(prices) < 2:
            return 0.0
        
        # Convert to pandas Series if needed
        if not isinstance(prices, pd.Series):
            prices = pd.Series(prices)
        
        # Calculate returns
        returns = prices.pct_change().dropna()
        
        if len(returns) == 0:
            return 0.0
        
        # Calculate VaR
        return float(np.percentile(returns, (1 - confidence) * 100))
    except Exception as e:
        print(f"Error calculating VaR: {e}")
        return 0.0

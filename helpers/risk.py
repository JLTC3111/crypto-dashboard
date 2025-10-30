import numpy as np

def max_drawdown(prices):
    peak = prices.cummax()
    dd = (prices - peak) / peak
    return dd.min()

def sharpe_ratio(prices, risk_free_rate=0.01):
    daily_returns = prices.pct_change().dropna()
    excess_returns = daily_returns - (risk_free_rate / 252)
    return excess_returns.mean() / excess_returns.std() * np.sqrt(252)

def value_at_risk(prices, confidence=0.95):
    returns = prices.pct_change().dropna()
    return np.percentile(returns, (1 - confidence) * 100)

"""
Portfolio Analytics Module
Provides advanced analytics and calculations for cryptocurrency portfolios
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class PortfolioMetrics:
    """Calculate various portfolio performance metrics"""
    
    @staticmethod
    def calculate_returns(prices: pd.Series, period: str = 'daily') -> pd.Series:
        """
        Calculate returns for a given price series
        
        Args:
            prices: Price series
            period: 'daily', 'weekly', 'monthly', or 'yearly'
        
        Returns:
            pd.Series: Returns for the specified period
        """
        try:
            if period == 'daily':
                return prices.pct_change()
            elif period == 'weekly':
                return prices.resample('W').last().pct_change()
            elif period == 'monthly':
                return prices.resample('M').last().pct_change()
            elif period == 'yearly':
                return prices.resample('Y').last().pct_change()
            else:
                return prices.pct_change()
        except Exception as e:
            print(f"Error calculating returns: {e}")
            return pd.Series()
    
    @staticmethod
    def calculate_volatility(prices: pd.Series, window: int = 30) -> float:
        """
        Calculate rolling volatility
        
        Args:
            prices: Price series
            window: Rolling window in days
        
        Returns:
            float: Annualized volatility
        """
        try:
            returns = prices.pct_change().dropna()
            if len(returns) < window:
                return returns.std() * np.sqrt(252)
            return returns.rolling(window).std().iloc[-1] * np.sqrt(252)
        except Exception as e:
            print(f"Error calculating volatility: {e}")
            return 0.0
    
    @staticmethod
    def calculate_beta(asset_returns: pd.Series, market_returns: pd.Series) -> float:
        """
        Calculate beta coefficient against market
        
        Args:
            asset_returns: Asset return series
            market_returns: Market return series
        
        Returns:
            float: Beta coefficient
        """
        try:
            # Align the series
            aligned_df = pd.concat([asset_returns, market_returns], axis=1, join='inner')
            if len(aligned_df) < 2:
                return 1.0
            
            covariance = aligned_df.cov().iloc[0, 1]
            market_variance = market_returns.var()
            
            if market_variance == 0:
                return 1.0
            
            return covariance / market_variance
        except Exception as e:
            print(f"Error calculating beta: {e}")
            return 1.0
    
    @staticmethod
    def calculate_correlation_matrix(returns_dict: Dict[str, pd.Series]) -> pd.DataFrame:
        """
        Calculate correlation matrix for multiple assets
        
        Args:
            returns_dict: Dictionary of asset names to return series
        
        Returns:
            pd.DataFrame: Correlation matrix
        """
        try:
            if not returns_dict:
                return pd.DataFrame()
            
            returns_df = pd.DataFrame(returns_dict)
            return returns_df.corr()
        except Exception as e:
            print(f"Error calculating correlation matrix: {e}")
            return pd.DataFrame()


class PortfolioOptimizer:
    """Portfolio optimization utilities"""
    
    @staticmethod
    def calculate_portfolio_weights(
        assets: List[str],
        target_return: Optional[float] = None,
        risk_tolerance: str = 'medium'
    ) -> Dict[str, float]:
        """
        Calculate optimal portfolio weights based on risk tolerance
        
        Args:
            assets: List of asset symbols
            target_return: Target portfolio return
            risk_tolerance: 'low', 'medium', or 'high'
        
        Returns:
            Dict: Optimal weights for each asset
        """
        try:
            # Simplified weight allocation based on risk tolerance
            n_assets = len(assets)
            if n_assets == 0:
                return {}
            
            if risk_tolerance == 'low':
                # Conservative: Equal weight with slight bias to less volatile assets
                base_weight = 0.8 / n_assets
                stable_weight = 0.2
                weights = {asset: base_weight for asset in assets}
                # Add extra weight to first asset (assuming it's more stable)
                if assets:
                    weights[assets[0]] += stable_weight
            elif risk_tolerance == 'high':
                # Aggressive: Higher concentration in top performers
                weights = {}
                for i, asset in enumerate(assets):
                    if i == 0:
                        weights[asset] = 0.4
                    elif i == 1:
                        weights[asset] = 0.3
                    else:
                        weights[asset] = 0.3 / (n_assets - 2) if n_assets > 2 else 0.3
            else:  # medium
                # Balanced: Equal weight distribution
                equal_weight = 1.0 / n_assets
                weights = {asset: equal_weight for asset in assets}
            
            return weights
        except Exception as e:
            print(f"Error calculating portfolio weights: {e}")
            return {asset: 1.0/len(assets) for asset in assets} if assets else {}
    
    @staticmethod
    def rebalance_portfolio(
        current_holdings: Dict[str, float],
        target_weights: Dict[str, float],
        total_value: float
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculate rebalancing actions needed
        
        Args:
            current_holdings: Current holdings {asset: value}
            target_weights: Target portfolio weights {asset: weight}
            total_value: Total portfolio value
        
        Returns:
            Dict: Rebalancing actions for each asset
        """
        try:
            actions = {}
            
            for asset, target_weight in target_weights.items():
                target_value = total_value * target_weight
                current_value = current_holdings.get(asset, 0)
                difference = target_value - current_value
                
                actions[asset] = {
                    'current_value': current_value,
                    'target_value': target_value,
                    'difference': difference,
                    'action': 'BUY' if difference > 0 else 'SELL' if difference < 0 else 'HOLD',
                    'amount': abs(difference)
                }
            
            return actions
        except Exception as e:
            print(f"Error calculating rebalancing actions: {e}")
            return {}


class RiskAnalyzer:
    """Advanced risk analysis for portfolios"""
    
    @staticmethod
    def calculate_conditional_var(
        returns: pd.Series,
        confidence: float = 0.95
    ) -> float:
        """
        Calculate Conditional Value at Risk (CVaR)
        
        Args:
            returns: Return series
            confidence: Confidence level
        
        Returns:
            float: CVaR value
        """
        try:
            if returns is None or len(returns) == 0:
                return 0.0
            
            var_threshold = returns.quantile(1 - confidence)
            conditional_returns = returns[returns <= var_threshold]
            
            if len(conditional_returns) == 0:
                return var_threshold
            
            return conditional_returns.mean()
        except Exception as e:
            print(f"Error calculating CVaR: {e}")
            return 0.0
    
    @staticmethod
    def calculate_sortino_ratio(
        returns: pd.Series,
        target_return: float = 0,
        risk_free_rate: float = 0.02
    ) -> float:
        """
        Calculate Sortino ratio (downside risk-adjusted return)
        
        Args:
            returns: Return series
            target_return: Target return threshold
            risk_free_rate: Risk-free rate
        
        Returns:
            float: Sortino ratio
        """
        try:
            if returns is None or len(returns) < 2:
                return 0.0
            
            excess_returns = returns - risk_free_rate/252
            downside_returns = excess_returns[excess_returns < target_return]
            
            if len(downside_returns) == 0:
                return 0.0
            
            downside_deviation = np.sqrt(np.mean(downside_returns**2))
            
            if downside_deviation == 0:
                return 0.0
            
            return (excess_returns.mean() - target_return) / downside_deviation * np.sqrt(252)
        except Exception as e:
            print(f"Error calculating Sortino ratio: {e}")
            return 0.0
    
    @staticmethod
    def calculate_calmar_ratio(
        returns: pd.Series,
        prices: pd.Series,
        period_years: float = 3
    ) -> float:
        """
        Calculate Calmar ratio (return over maximum drawdown)
        
        Args:
            returns: Return series
            prices: Price series
            period_years: Period in years
        
        Returns:
            float: Calmar ratio
        """
        try:
            if returns is None or len(returns) == 0:
                return 0.0
            
            # Calculate annualized return
            total_return = (prices.iloc[-1] / prices.iloc[0]) - 1
            annualized_return = (1 + total_return) ** (1/period_years) - 1
            
            # Calculate maximum drawdown
            rolling_max = prices.cummax()
            drawdown = (prices - rolling_max) / rolling_max
            max_drawdown = drawdown.min()
            
            if max_drawdown == 0:
                return 0.0
            
            return annualized_return / abs(max_drawdown)
        except Exception as e:
            print(f"Error calculating Calmar ratio: {e}")
            return 0.0


class PortfolioAnalytics:
    """Main portfolio analytics interface"""
    
    def __init__(self):
        self.metrics = PortfolioMetrics()
        self.optimizer = PortfolioOptimizer()
        self.risk_analyzer = RiskAnalyzer()
    
    def analyze_portfolio(
        self,
        holdings: Dict[str, float],
        prices: Dict[str, pd.Series]
    ) -> Dict[str, Any]:
        """
        Comprehensive portfolio analysis
        
        Args:
            holdings: Current holdings {asset: quantity}
            prices: Price history for each asset
        
        Returns:
            Dict: Complete portfolio analysis
        """
        try:
            analysis = {
                'total_value': 0,
                'assets': {},
                'portfolio_metrics': {},
                'risk_metrics': {},
                'allocation': {}
            }
            
            # Calculate individual asset metrics
            for asset, quantity in holdings.items():
                if asset in prices:
                    current_price = prices[asset].iloc[-1]
                    value = quantity * current_price
                    analysis['total_value'] += value
                    
                    analysis['assets'][asset] = {
                        'quantity': quantity,
                        'current_price': current_price,
                        'value': value,
                        'returns': self.metrics.calculate_returns(prices[asset]),
                        'volatility': self.metrics.calculate_volatility(prices[asset])
                    }
            
            # Calculate portfolio-level metrics
            if analysis['total_value'] > 0:
                # Calculate weights
                for asset in analysis['assets']:
                    weight = analysis['assets'][asset]['value'] / analysis['total_value']
                    analysis['allocation'][asset] = weight
                
                # Risk metrics
                if prices:
                    portfolio_returns = self._calculate_portfolio_returns(holdings, prices)
                    analysis['risk_metrics'] = {
                        'sortino_ratio': self.risk_analyzer.calculate_sortino_ratio(portfolio_returns),
                        'conditional_var': self.risk_analyzer.calculate_conditional_var(portfolio_returns)
                    }
            
            return analysis
        except Exception as e:
            print(f"Error analyzing portfolio: {e}")
            return {}
    
    def _calculate_portfolio_returns(
        self,
        holdings: Dict[str, float],
        prices: Dict[str, pd.Series]
    ) -> pd.Series:
        """Calculate portfolio-level returns"""
        try:
            # Calculate weighted returns
            total_value = sum(holdings[asset] * prices[asset].iloc[-1] 
                            for asset in holdings if asset in prices)
            
            if total_value == 0:
                return pd.Series()
            
            weighted_returns = pd.Series(dtype=float)
            for asset, quantity in holdings.items():
                if asset in prices:
                    weight = (quantity * prices[asset].iloc[-1]) / total_value
                    asset_returns = prices[asset].pct_change().dropna()
                    if weighted_returns.empty:
                        weighted_returns = asset_returns * weight
                    else:
                        weighted_returns = weighted_returns.add(asset_returns * weight, fill_value=0)
            
            return weighted_returns
        except Exception as e:
            print(f"Error calculating portfolio returns: {e}")
            return pd.Series()


# Convenience functions for direct import
def analyze_portfolio(holdings: Dict[str, float], prices: Dict[str, pd.Series]) -> Dict[str, Any]:
    """Analyze portfolio performance and risk metrics"""
    analyzer = PortfolioAnalytics()
    return analyzer.analyze_portfolio(holdings, prices)


def optimize_weights(assets: List[str], risk_tolerance: str = 'medium') -> Dict[str, float]:
    """Get optimal portfolio weights based on risk tolerance"""
    optimizer = PortfolioOptimizer()
    return optimizer.calculate_portfolio_weights(assets, risk_tolerance=risk_tolerance)


def calculate_rebalancing(
    current_holdings: Dict[str, float],
    target_weights: Dict[str, float],
    total_value: float
) -> Dict[str, Dict[str, Any]]:
    """Calculate required rebalancing actions"""
    optimizer = PortfolioOptimizer()
    return optimizer.rebalance_portfolio(current_holdings, target_weights, total_value)
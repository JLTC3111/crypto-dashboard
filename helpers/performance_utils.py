"""
Performance Optimization Utilities
Provides caching, memoization, and performance monitoring tools
"""

import streamlit as st
import time
import functools
from typing import Callable, Any, Dict, Optional
import pandas as pd
from datetime import datetime, timedelta


class PerformanceMonitor:
    """Monitor and log performance metrics"""
    
    def __init__(self):
        if 'performance_metrics' not in st.session_state:
            st.session_state.performance_metrics = {}
    
    def track_execution_time(self, func_name: str, execution_time: float):
        """Track function execution time"""
        if func_name not in st.session_state.performance_metrics:
            st.session_state.performance_metrics[func_name] = {
                'count': 0,
                'total_time': 0,
                'avg_time': 0,
                'min_time': float('inf'),
                'max_time': 0
            }
        
        metrics = st.session_state.performance_metrics[func_name]
        metrics['count'] += 1
        metrics['total_time'] += execution_time
        metrics['avg_time'] = metrics['total_time'] / metrics['count']
        metrics['min_time'] = min(metrics['min_time'], execution_time)
        metrics['max_time'] = max(metrics['max_time'], execution_time)
    
    def get_metrics(self, func_name: Optional[str] = None) -> Dict:
        """Get performance metrics"""
        if func_name:
            return st.session_state.performance_metrics.get(func_name, {})
        return st.session_state.performance_metrics
    
    def display_metrics(self):
        """Display performance metrics in Streamlit"""
        if not st.session_state.performance_metrics:
            st.info("No performance metrics available yet")
            return
        
        st.subheader("⚡ Performance Metrics")
        
        metrics_df = pd.DataFrame([
            {
                'Function': func_name,
                'Calls': metrics['count'],
                'Avg Time (s)': f"{metrics['avg_time']:.4f}",
                'Min Time (s)': f"{metrics['min_time']:.4f}",
                'Max Time (s)': f"{metrics['max_time']:.4f}",
                'Total Time (s)': f"{metrics['total_time']:.2f}"
            }
            for func_name, metrics in st.session_state.performance_metrics.items()
        ])
        
        st.dataframe(metrics_df, use_container_width=True)


def timed_execution(func: Callable) -> Callable:
    """
    Decorator to track function execution time
    
    Usage:
        @timed_execution
        def my_function():
            ...
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        monitor = PerformanceMonitor()
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            execution_time = time.time() - start_time
            monitor.track_execution_time(func.__name__, execution_time)
    
    return wrapper


class DataFrameOptimizer:
    """Optimize DataFrame operations for better performance"""
    
    @staticmethod
    def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize DataFrame dtypes to reduce memory usage
        
        Args:
            df: Input DataFrame
        
        Returns:
            Optimized DataFrame
        """
        df_optimized = df.copy()
        
        for col in df_optimized.columns:
            col_type = df_optimized[col].dtype
            
            # Optimize numeric columns
            if col_type == 'float64':
                df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='float')
            elif col_type == 'int64':
                df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='integer')
            
            # Convert object columns to category if beneficial
            elif col_type == 'object':
                num_unique = df_optimized[col].nunique()
                num_total = len(df_optimized[col])
                
                # If less than 50% unique values, convert to category
                if num_unique / num_total < 0.5:
                    df_optimized[col] = df_optimized[col].astype('category')
        
        return df_optimized
    
    @staticmethod
    def get_memory_usage(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get detailed memory usage information
        
        Args:
            df: Input DataFrame
        
        Returns:
            Dictionary with memory usage details
        """
        memory_usage = df.memory_usage(deep=True)
        
        return {
            'total_mb': memory_usage.sum() / 1024**2,
            'per_column': {
                col: f"{memory_usage[col] / 1024**2:.2f} MB"
                for col in df.columns
            },
            'shape': df.shape,
            'dtypes': df.dtypes.to_dict()
        }


class CacheManager:
    """Manage Streamlit cache operations"""
    
    @staticmethod
    def clear_all_caches():
        """Clear all Streamlit caches"""
        st.cache_data.clear()
        st.cache_resource.clear()
    
    @staticmethod
    def clear_data_cache():
        """Clear only data cache"""
        st.cache_data.clear()
    
    @staticmethod
    def clear_resource_cache():
        """Clear only resource cache"""
        st.cache_resource.clear()
    
    @staticmethod
    def get_cache_stats() -> Dict[str, Any]:
        """Get cache statistics"""
        # Note: Streamlit doesn't provide direct cache stats API
        # This is a placeholder for future implementation
        return {
            'status': 'Cache stats not available in current Streamlit version',
            'recommendation': 'Use st.cache_data and st.cache_resource decorators'
        }


class BatchProcessor:
    """Process data in batches for better performance"""
    
    @staticmethod
    def process_in_batches(
        data: list,
        batch_size: int,
        process_func: Callable,
        show_progress: bool = True
    ) -> list:
        """
        Process data in batches with optional progress bar
        
        Args:
            data: List of items to process
            batch_size: Size of each batch
            process_func: Function to apply to each batch
            show_progress: Whether to show progress bar
        
        Returns:
            List of processed results
        """
        results = []
        total_batches = (len(data) + batch_size - 1) // batch_size
        
        if show_progress:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            batch_results = process_func(batch)
            results.extend(batch_results)
            
            if show_progress:
                progress = (i + batch_size) / len(data)
                progress_bar.progress(min(progress, 1.0))
                status_text.text(f"Processing batch {i//batch_size + 1}/{total_batches}")
        
        if show_progress:
            progress_bar.empty()
            status_text.empty()
        
        return results


class LazyLoader:
    """Lazy load data only when needed"""
    
    def __init__(self, load_func: Callable):
        self.load_func = load_func
        self._data = None
        self._loaded = False
    
    @property
    def data(self):
        """Get data, loading if necessary"""
        if not self._loaded:
            self._data = self.load_func()
            self._loaded = True
        return self._data
    
    def reload(self):
        """Force reload of data"""
        self._loaded = False
        return self.data
    
    def is_loaded(self) -> bool:
        """Check if data is loaded"""
        return self._loaded


def debounce(wait_time: float):
    """
    Debounce decorator to limit function calls
    
    Args:
        wait_time: Time to wait in seconds
    
    Usage:
        @debounce(0.5)
        def search_function(query):
            ...
    """
    def decorator(func: Callable) -> Callable:
        last_called = [0.0]
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            
            if current_time - last_called[0] >= wait_time:
                last_called[0] = current_time
                return func(*args, **kwargs)
            
        return wrapper
    return decorator


def memoize_with_ttl(ttl_seconds: int):
    """
    Memoization decorator with time-to-live
    
    Args:
        ttl_seconds: Time to live in seconds
    
    Usage:
        @memoize_with_ttl(300)
        def expensive_function(arg):
            ...
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            current_time = time.time()
            
            if key in cache:
                result, timestamp = cache[key]
                if current_time - timestamp < ttl_seconds:
                    return result
            
            result = func(*args, **kwargs)
            cache[key] = (result, current_time)
            return result
        
        return wrapper
    return decorator


# Export main components
__all__ = [
    'PerformanceMonitor',
    'timed_execution',
    'DataFrameOptimizer',
    'CacheManager',
    'BatchProcessor',
    'LazyLoader',
    'debounce',
    'memoize_with_ttl'
]

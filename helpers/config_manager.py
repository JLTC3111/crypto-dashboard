"""
Configuration Management Module
Centralized configuration for the entire application
"""

import streamlit as st
from typing import Any, Dict, Optional
import json
from pathlib import Path


class Config:
    """Application configuration manager"""
    
    # Default configuration
    DEFAULT_CONFIG = {
        # API Settings
        'api': {
            'coingecko_rate_limit': 50,  # requests per minute
            'binance_timeout': 10,  # seconds
            'retry_attempts': 3,
            'retry_delay': 2,  # seconds
        },
        
        # Cache Settings
        'cache': {
            'price_history_ttl': 1800,  # 30 minutes
            'current_prices_ttl': 60,  # 1 minute
            'market_data_ttl': 300,  # 5 minutes
            'news_ttl': 300,  # 5 minutes
        },
        
        # Display Settings
        'display': {
            'default_coins': 100,
            'max_coins': 500,
            'table_height': 500,
            'chart_height': 400,
            'decimal_places': 2,
            'large_number_format': 'abbreviated',  # 'full' or 'abbreviated'
        },
        
        # Risk Calculation Settings
        'risk': {
            'default_risk_free_rate': 0.02,  # 2%
            'var_confidence': 0.95,  # 95%
            'sharpe_periods': 252,  # trading days per year
            'volatility_window': 30,  # days
        },
        
        # Portfolio Settings
        'portfolio': {
            'default_currency': 'USD',
            'rebalance_threshold': 0.05,  # 5%
            'min_position_size': 0.01,  # 1%
            'max_position_size': 0.30,  # 30%
        },
        
        # Theme Settings
        'theme': {
            'default_theme': 'dark',
            'enable_animations': True,
            'chart_style': 'modern',
        },
        
        # Language Settings
        'language': {
            'default_language': 'en',
            'fallback_language': 'en',
        },
        
        # Performance Settings
        'performance': {
            'enable_profiling': False,
            'log_slow_queries': True,
            'slow_query_threshold': 5.0,  # seconds
            'batch_size': 100,
        },
        
        # Data Validation
        'validation': {
            'min_data_points': 30,
            'max_missing_data_pct': 0.10,  # 10%
            'outlier_threshold': 3.0,  # standard deviations
        },
    }
    
    @staticmethod
    def get(key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key_path: Configuration key path (e.g., 'api.retry_attempts')
            default: Default value if key not found
        
        Returns:
            Configuration value
        
        Example:
            >>> Config.get('api.retry_attempts')
            3
        """
        # Initialize config in session state if not exists
        if 'app_config' not in st.session_state:
            st.session_state.app_config = Config.DEFAULT_CONFIG.copy()
        
        # Navigate through nested dict using dot notation
        keys = key_path.split('.')
        value = st.session_state.app_config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    @staticmethod
    def set(key_path: str, value: Any):
        """
        Set configuration value using dot notation
        
        Args:
            key_path: Configuration key path
            value: Value to set
        
        Example:
            >>> Config.set('api.retry_attempts', 5)
        """
        if 'app_config' not in st.session_state:
            st.session_state.app_config = Config.DEFAULT_CONFIG.copy()
        
        keys = key_path.split('.')
        config = st.session_state.app_config
        
        # Navigate to the parent dict
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the value
        config[keys[-1]] = value
    
    @staticmethod
    def get_section(section: str) -> Dict[str, Any]:
        """
        Get entire configuration section
        
        Args:
            section: Section name (e.g., 'api', 'cache')
        
        Returns:
            Dictionary of section configuration
        """
        if 'app_config' not in st.session_state:
            st.session_state.app_config = Config.DEFAULT_CONFIG.copy()
        
        return st.session_state.app_config.get(section, {})
    
    @staticmethod
    def update_section(section: str, updates: Dict[str, Any]):
        """
        Update entire configuration section
        
        Args:
            section: Section name
            updates: Dictionary of updates
        """
        if 'app_config' not in st.session_state:
            st.session_state.app_config = Config.DEFAULT_CONFIG.copy()
        
        if section not in st.session_state.app_config:
            st.session_state.app_config[section] = {}
        
        st.session_state.app_config[section].update(updates)
    
    @staticmethod
    def reset():
        """Reset configuration to defaults"""
        st.session_state.app_config = Config.DEFAULT_CONFIG.copy()
    
    @staticmethod
    def export_config() -> str:
        """Export configuration as JSON string"""
        if 'app_config' not in st.session_state:
            st.session_state.app_config = Config.DEFAULT_CONFIG.copy()
        
        return json.dumps(st.session_state.app_config, indent=2)
    
    @staticmethod
    def import_config(config_json: str):
        """
        Import configuration from JSON string
        
        Args:
            config_json: JSON string of configuration
        """
        try:
            config = json.loads(config_json)
            st.session_state.app_config = config
            return True
        except json.JSONDecodeError as e:
            st.error(f"Invalid configuration JSON: {e}")
            return False
    
    @staticmethod
    def save_to_file(filepath: str):
        """
        Save configuration to file
        
        Args:
            filepath: Path to save configuration
        """
        config_json = Config.export_config()
        Path(filepath).write_text(config_json)
    
    @staticmethod
    def load_from_file(filepath: str):
        """
        Load configuration from file
        
        Args:
            filepath: Path to configuration file
        """
        try:
            config_json = Path(filepath).read_text()
            return Config.import_config(config_json)
        except FileNotFoundError:
            st.error(f"Configuration file not found: {filepath}")
            return False


def create_config_editor():
    """Create an interactive configuration editor"""
    st.subheader("⚙️ Configuration Editor")
    
    # Get current config
    if 'app_config' not in st.session_state:
        st.session_state.app_config = Config.DEFAULT_CONFIG.copy()
    
    # Create tabs for different sections
    sections = list(Config.DEFAULT_CONFIG.keys())
    tabs = st.tabs(sections)
    
    for i, section in enumerate(sections):
        with tabs[i]:
            st.markdown(f"### {section.title()} Settings")
            
            section_config = Config.get_section(section)
            
            for key, value in section_config.items():
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.write(f"**{key.replace('_', ' ').title()}**")
                
                with col2:
                    # Determine input type based on value type
                    if isinstance(value, bool):
                        new_value = st.checkbox(
                            f"{section}.{key}",
                            value=value,
                            key=f"config_{section}_{key}",
                            label_visibility="collapsed"
                        )
                    elif isinstance(value, int):
                        new_value = st.number_input(
                            f"{section}.{key}",
                            value=value,
                            key=f"config_{section}_{key}",
                            label_visibility="collapsed"
                        )
                    elif isinstance(value, float):
                        new_value = st.number_input(
                            f"{section}.{key}",
                            value=value,
                            format="%.4f",
                            key=f"config_{section}_{key}",
                            label_visibility="collapsed"
                        )
                    elif isinstance(value, str):
                        new_value = st.text_input(
                            f"{section}.{key}",
                            value=value,
                            key=f"config_{section}_{key}",
                            label_visibility="collapsed"
                        )
                    else:
                        new_value = value
                    
                    # Update if changed
                    if new_value != value:
                        Config.set(f"{section}.{key}", new_value)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Export Config"):
            config_json = Config.export_config()
            st.download_button(
                "Download Configuration",
                config_json,
                file_name="dashboard_config.json",
                mime="application/json"
            )
    
    with col2:
        uploaded_file = st.file_uploader("📁 Import Config", type=['json'])
        if uploaded_file:
            config_json = uploaded_file.read().decode()
            if Config.import_config(config_json):
                st.success("Configuration imported successfully!")
                st.rerun()
    
    with col3:
        if st.button("🔄 Reset to Defaults"):
            Config.reset()
            st.success("Configuration reset to defaults!")
            st.rerun()


# Convenience functions
def get_config(key: str, default: Any = None) -> Any:
    """Shorthand for Config.get()"""
    return Config.get(key, default)


def set_config(key: str, value: Any):
    """Shorthand for Config.set()"""
    Config.set(key, value)


# Export main components
__all__ = [
    'Config',
    'create_config_editor',
    'get_config',
    'set_config'
]

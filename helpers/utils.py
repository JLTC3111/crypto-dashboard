"""
Utility functions for formatting and common operations
"""

def format_currency(value: float) -> str:
    """Format a numeric value as currency"""
    if value is None or not isinstance(value, (int, float)):
        return "$0.00"
    
    if abs(value) >= 1e12:
        return f"${value/1e12:.1f}T"
    elif abs(value) >= 1e9:
        return f"${value/1e9:.1f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.1f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.1f}K"
    else:
        return f"${value:,.2f}"

def format_percentage(value: float) -> str:
    """Format a numeric value as a percentage"""
    if value is None or not isinstance(value, (int, float)):
        return "0.00%"
    return f"{value:.2f}%"

def format_number(value: float, decimals: int = 2) -> str:
    """Format a number with proper comma separators"""
    if value is None or not isinstance(value, (int, float)):
        return "0"
    return f"{value:,.{decimals}f}"

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero"""
    if denominator == 0 or denominator is None:
        return default
    return numerator / denominator

def truncate_string(text: str, max_length: int = 50) -> str:
    """Truncate a string to a maximum length with ellipsis"""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
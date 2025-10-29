"""
SVG Icon System for Streamlit Dashboard
Replace emoji usage with proper SVG icons for better performance and consistency
"""

def get_svg_icon(icon_name: str, size: int = 24, color: str = "#000000") -> str:
    """
    Get SVG icon as HTML string for Streamlit
    
    Args:
        icon_name: Name of the icon
        size: Icon size in pixels
        color: Icon color in hex format
    
    Returns:
        HTML string with inline SVG icon
    """
    
    icons = {
        # Dashboard & Analytics Icons
        "dashboard": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>',
        "chart": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        "analytics": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><polyline points="9,10 12,7 16,11 21,6"/></svg>',
        
        # Finance Icons
        "scale": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/></svg>',
        "trending-down": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22,17 13.5,8.5 8.5,13.5 2,7"/><polyline points="16,17 22,17 22,11"/></svg>',
        "value-at-risk": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/></svg>',
        
        # Admin & Tools Icons
        "wrench": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
        "settings": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v6m0 6v6m4.22-13.22 4.24 4.24M1.54 12H7.5m8.5 0h6M4.22 19.78l4.24-4.24m10.61 0 4.24 4.24M1.54 12H7.5"/></svg>',
        
        # Nature Icons
        "wave": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 10s2-2 5-2 5 2 8 2 5-2 8-2"/><path d="M2 17s2-2 5-2 5 2 8 2 5-2 8-2"/></svg>',
        "water": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
        
        # Media Icons
        "news": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/><path d="M9 10h6"/><path d="M9 14h6"/><path d="M9 18h6"/></svg>',
        "newspaper": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/><path d="M18 14h-6"/><path d="M15 18h-3"/><path d="M10 6h8v4h-8V6Z"/></svg>',
        
        # Fun/Misc Icons
        "playground": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 4v7a1 1 0 0 0 1 1h7"/><path d="M18 8h-3.5a1.5 1.5 0 0 0 0 3h2a1.5 1.5 0 0 1 0 3H13"/><path d="m12 2-7 8v11h18V10l-7-8Z"/></svg>',
        
        # Status Icons
        "success": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22,4 12,14.01 9,11.01"/></svg>',
        "warning": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        "danger": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="7.86,2 16.14,2 22,7.86 22,16.14 16.14,22 7.86,22 2,16.14 2,7.86 7.86,2"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
        
        # Financial Risk Icons
        "sharpe-ratio": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        "max-drawdown": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 12l5 5 5-5"/></svg>',
        
        # Currency Icons
        "dollar": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        
        # Additional Icons for Metrics
        "refresh": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23,4 23,10 17,10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36l2.63 2.63"/></svg>',
        "settings-gear": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v6m0 6v6m4.22-13.22 4.24 4.24M1.54 12h6m6 0h6M4.22 19.78l4.24-4.24m10.6 0 4.24 4.24M1.54 12h6"/></svg>',
    }
    
    return icons.get(icon_name, f'<span style="color: {color};">•</span>')


def icon_with_text(icon_name: str, text: str, size: int = 16, color: str = "#000000") -> str:
    """
    Combine SVG icon with text for display
    
    Args:
        icon_name: Name of the icon
        text: Text to display after icon
        size: Icon size in pixels
        color: Icon color in hex format
    
    Returns:
        HTML string with icon and text
    """
    icon = get_svg_icon(icon_name, size, color)
    return f'<span style="display: inline-flex; align-items: center; gap: 8px;">{icon} <span>{text}</span></span>'


# Mapping of emoji to SVG icon names for easy replacement
EMOJI_TO_ICON_MAP = {
    "📊": "chart",
    "⚖️": "scale",
    "🛝": "playground",
    "🔧": "wrench",
    "🌊": "wave",
    "📰": "newspaper",
    "💰": "dollar",
    "📉": "trending-down",
    "📈": "chart",
    "✅": "success",
    "⚠️": "warning",
    "🚨": "danger",
}

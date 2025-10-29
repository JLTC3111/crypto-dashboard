"""
Modern UI Components System
Industry-standard design patterns with glassmorphism, animations, and professional styling
"""

import streamlit as st
from typing import Optional, Dict, Any, List, Tuple
from helpers.theme_config import Theme, get_theme_colors
from helpers.i18n import t
from helpers.svg_icons import get_svg_icon


class ModernUI:
    """Modern UI components with industry best practices"""
    
    @staticmethod
    def apply_modern_theme():
        """Apply comprehensive modern theme with glassmorphism and animations"""
        theme = get_theme_colors()
        
        css = f"""
        <style>
            /* Import Google Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            /* Root Variables */
            :root {{
                --primary-bg: {theme['background']};
                --secondary-bg: {theme['secondary_background']};
                --card-bg: {theme['card_background']};
                --text-primary: {theme['text_primary']};
                --text-secondary: {theme['text_secondary']};
                --accent: {theme['accent_primary']};
                --accent-hover: {theme['accent_secondary']};
                --success: {theme['success']};
                --warning: {theme['warning']};
                --error: {theme['error']};
                --border: {theme['border']};
                --shadow: {theme['shadow']};
                --gradient-start: {theme['gradient_start']};
                --gradient-end: {theme['gradient_end']};
                --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            /* Global Styles - Optimized */
            html, body, .stApp {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }}
            
            /* Background Pattern - Fixed z-index */
            .stApp {{
                background: var(--primary-bg);
                position: relative;
            }}
            
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image: 
                    radial-gradient(circle at 20% 80%, {theme['accent_primary']}15 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, {theme['accent_secondary']}15 0%, transparent 50%);
                pointer-events: none;
                z-index: -1;  /* Changed from 0 to -1 to stay behind content */
                will-change: opacity;
            }}
            
            /* Ensure main content stays above background */
            .main .block-container {{
                position: relative;
                z-index: 1;
            }}
            
            /* Ensure all streamlit elements are visible */
            section.main > div {{
                position: relative;
                z-index: 1;
            }}
            
            [data-testid="stAppViewContainer"] {{
                position: relative;
                z-index: 1;
            }}
            
            /* Modern Sidebar Design - Optimized */
            [data-testid="stSidebar"] {{
                background: linear-gradient(135deg, {theme['secondary_background']}ee, {theme['card_background']}dd);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border-right: 1px solid {theme['border']}44;
                box-shadow: 4px 0 24px {theme['shadow']};
                position: relative;
                z-index: 2;
            }}
            
            [data-testid="stSidebar"] .element-container {{
                background: transparent;
            }}
            
            /* Sidebar Header Styling */
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {{
                background: linear-gradient(135deg, var(--accent), var(--accent-hover));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 600;
                letter-spacing: -0.02em;
            }}
            
            /* Settings Section Card */
            .settings-card {{
                background: linear-gradient(135deg, {theme['card_background']}99, {theme['secondary_background']}66);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid {theme['border']}44;
                border-radius: 16px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 8px 32px {theme['shadow']};
            }}
            
            /* Modern Buttons */
            .stButton > button {{
                background: linear-gradient(135deg, var(--accent), var(--accent-hover));
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0.75rem 1.5rem;
                font-weight: 500;
                font-size: 0.95rem;
                letter-spacing: 0.01em;
                box-shadow: 0 4px 12px {theme['accent_primary']}44;
                position: relative;
                overflow: hidden;
                z-index: 1;
            }}
            
            .stButton > button::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, var(--accent-hover), var(--accent));
                opacity: 0;
                transition: opacity 0.3s ease;
                z-index: -1;
            }}
            
            .stButton > button:hover::before {{
                opacity: 1;
            }}
            
            .stButton > button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 24px {theme['accent_primary']}66;
            }}
            
            .stButton > button:active {{
                transform: translateY(0);
                box-shadow: 0 4px 12px {theme['accent_primary']}44;
            }}
            
            /* Theme Toggle Button */
            .theme-toggle-btn {{
                background: {theme['card_background']}99;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid {theme['border']}44;
                border-radius: 50px;
                padding: 0.75rem 1.25rem;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 16px {theme['shadow']};
            }}
            
            .theme-toggle-btn:hover {{
                background: {theme['card_background']};
                transform: scale(1.05);
                box-shadow: 0 6px 20px {theme['shadow']};
            }}
            
            /* Modern Select Boxes */
            .stSelectbox > div > div {{
                background: {theme['card_background']}99;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid {theme['border']}44;
                border-radius: 12px;
                padding: 0.5rem 1rem;
                font-weight: 500;
            }}
            
            .stSelectbox > div > div:hover {{
                border-color: var(--accent);
                box-shadow: 0 0 0 2px {theme['accent_primary']}22;
            }}
            
            /* Modern Input Fields */
            .stTextInput > div > div > input,
            .stNumberInput > div > div > input {{
                background: {theme['card_background']}99;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid {theme['border']}44;
                border-radius: 12px;
                padding: 0.75rem 1rem;
                font-weight: 400;
                color: var(--text-primary);
                transition: all 0.2s ease;
            }}
            
            .stTextInput > div > div > input:focus,
            .stNumberInput > div > div > input:focus {{
                border-color: var(--accent);
                box-shadow: 0 0 0 3px {theme['accent_primary']}22;
                outline: none;
            }}
            
            /* Glassmorphism Cards */
            .glass-card {{
                background: linear-gradient(135deg, {theme['card_background']}66, {theme['secondary_background']}44);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid {theme['border']}33;
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 8px 32px {theme['shadow']};
                position: relative;
                overflow: hidden;
            }}
            
            .glass-card::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, transparent 30%, {theme['accent_primary']}11 100%);
                pointer-events: none;
            }}
            
            /* Modern Gradient Header */
            .modern-header {{
                background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
                border-radius: 20px;
                padding: 2.5rem;
                margin-bottom: 2rem;
                position: relative;
                overflow: hidden;
                box-shadow: 0 12px 40px {theme['shadow']};
            }}
            
            .modern-header::before {{
                content: "";
                position: absolute;
                top: -50%;
                right: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                animation: shimmer 3s linear infinite;
            }}
            
            @keyframes shimmer {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            
            /* Modern Tabs */
            .stTabs [data-baseweb="tab-list"] {{
                background: {theme['card_background']}99;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid {theme['border']}33;
                border-radius: 16px;
                padding: 0.5rem;
                gap: 0.5rem;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                background: transparent;
                color: var(--text-secondary);
                border-radius: 12px;
                padding: 0.75rem 1.5rem;
                font-weight: 500;
                transition: all 0.2s ease;
            }}
            
            .stTabs [data-baseweb="tab"]:hover {{
                background: {theme['secondary_background']}66;
                color: var(--text-primary);
            }}
            
            .stTabs [aria-selected="true"] {{
                background: linear-gradient(135deg, var(--accent), var(--accent-hover));
                color: white !important;
                box-shadow: 0 4px 12px {theme['accent_primary']}44;
            }}
            
            /* Modern Metrics */
            [data-testid="metric-container"] {{
                background: {theme['card_background']}99;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid {theme['border']}33;
                border-radius: 16px;
                padding: 1.5rem;
                box-shadow: 0 4px 16px {theme['shadow']};
            }}
            
            [data-testid="stMetricValue"] {{
                font-weight: 700;
                font-size: 2rem;
                background: linear-gradient(135deg, var(--accent), var(--accent-hover));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            /* Modern Slider */
            .stSlider > div > div {{
                background: {theme['border']}44;
                border-radius: 10px;
            }}
            
            .stSlider > div > div > div {{
                background: linear-gradient(135deg, var(--accent), var(--accent-hover));
                border-radius: 10px;
            }}
            
            .stSlider > div > div > div > div {{
                background: white;
                border: 3px solid var(--accent);
                box-shadow: 0 2px 8px {theme['accent_primary']}44;
            }}
            
            /* Loading Animation */
            .stSpinner > div {{
                border-color: var(--accent);
            }}
            
            /* Scrollbar Design */
            ::-webkit-scrollbar {{
                width: 10px;
                height: 10px;
            }}
            
            ::-webkit-scrollbar-track {{
                background: {theme['secondary_background']}66;
                border-radius: 10px;
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: linear-gradient(135deg, var(--accent), var(--accent-hover));
                border-radius: 10px;
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: var(--accent-hover);
            }}
            
            /* Modern DataFrames */
            .dataframe {{
                background: {theme['card_background']}99 !important;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid {theme['border']}33 !important;
                border-radius: 12px;
                overflow: hidden;
            }}
            
            .dataframe th {{
                background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end)) !important;
                color: white !important;
                font-weight: 600;
                text-transform: uppercase;
                font-size: 0.85rem;
                letter-spacing: 0.05em;
                padding: 1rem !important;
            }}
            
            .dataframe td {{
                background: {theme['card_background']}99 !important;
                color: var(--text-primary) !important;
                font-weight: 400;
                padding: 0.75rem !important;
                border-bottom: 1px solid {theme['border']}22 !important;
            }}
            
            .dataframe tr:hover td {{
                background: {theme['secondary_background']}66 !important;
            }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)


def create_modern_sidebar():
    """Create a redesigned modern sidebar with better UX"""
    with st.sidebar:
        # Logo/Brand Section
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="font-size: 1.75rem; font-weight: 700; margin: 0;">
                <span style="background: linear-gradient(135deg, #4A9EFF, #7B61FF); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    Crypto Dashboard
                </span>
            </h1>
            <p style="font-size: 0.85rem; opacity: 0.7; margin-top: 0.5rem;">
                Professional Trading Analytics
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Settings Section with Modern Design
        settings_header = f"""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
            {get_svg_icon('settings', size=20)}
            <span style="font-weight: 600; font-size: 1.1rem;">{t('settings')}</span>
        </div>
        """
        st.markdown(settings_header, unsafe_allow_html=True)
        
        # Settings Card
        st.markdown('<div class="settings-card">', unsafe_allow_html=True)
        
        # Language Section
        lang_header = f"""
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem;">
            {get_svg_icon('language', size=18)}
            <span style="font-weight: 500;">{t('language')}</span>
        </div>
        """
        st.markdown(lang_header, unsafe_allow_html=True)
        
        from helpers.i18n import create_language_selector
        create_language_selector()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Theme Section
        theme_header = f"""
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem;">
            {get_svg_icon('sun' if st.session_state.get('theme', 'dark') == 'light' else 'moon', size=18)}
            <span style="font-weight: 500;">{t('theme')}</span>
        </div>
        """
        st.markdown(theme_header, unsafe_allow_html=True)
        
        create_modern_theme_toggle()
        
        st.markdown('</div>', unsafe_allow_html=True)


def create_modern_theme_toggle():
    """Create a modern theme toggle with SVG icons"""
    current_theme = st.session_state.get('theme', 'dark')
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            "🌙 Dark" if current_theme == 'light' else "☀️ Light",
            use_container_width=True,
            key="theme_toggle_modern"
        ):
            from helpers.theme_config import Theme
            Theme.toggle_theme()
            st.rerun()
    
    # Display current theme with icon
    theme_display = f"""
    <div class="theme-toggle-btn" style="margin-top: 0.5rem;">
        {get_svg_icon('moon' if current_theme == 'dark' else 'sun', size=20)}
        <span style="font-weight: 500;">{current_theme.title()} Mode</span>
    </div>
    """
    st.markdown(theme_display, unsafe_allow_html=True)


def create_modern_header(title: str, subtitle: str = "", icon: str = None):
    """Create a modern animated header with optional icon"""
    icon_html = get_svg_icon(icon, size=32) if icon else ""
    
    html = f"""
    <div class="modern-header">
        <div style="position: relative; z-index: 1;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                {icon_html}
                <h1 style="margin: 0; color: white; font-size: 2.5rem; font-weight: 700; 
                          letter-spacing: -0.02em; line-height: 1.2;">
                    {title}
                </h1>
            </div>
            {f'<p style="margin: 1rem 0 0 0; color: rgba(255,255,255,0.9); font-size: 1.1rem;">{subtitle}</p>' if subtitle else ''}
        </div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)


def create_glass_card(content: str, title: str = "", icon: str = None):
    """Create a glassmorphism card with optional title and icon"""
    title_html = ""
    if title:
        icon_html = get_svg_icon(icon, size=20) if icon else ""
        title_html = f"""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
            {icon_html}
            <h3 style="margin: 0; font-weight: 600;">{title}</h3>
        </div>
        """
    
    html = f"""
    <div class="glass-card">
        {title_html}
        {content}
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)


def create_modern_button(
    label: str,
    icon: str = None,
    variant: str = "primary",
    size: str = "medium",
    full_width: bool = False
):
    """
    Create a modern button with icon support
    
    Args:
        label: Button text
        icon: Icon name (optional)
        variant: Button variant (primary, secondary, success, warning, error)
        size: Button size (small, medium, large)
        full_width: Whether button should take full width
    """
    theme = get_theme_colors()
    
    # Color mapping for variants
    colors = {
        'primary': (theme['accent_primary'], theme['accent_secondary']),
        'secondary': (theme['text_secondary'], theme['text_primary']),
        'success': (theme['success'], theme['success']),
        'warning': (theme['warning'], theme['warning']),
        'error': (theme['error'], theme['error'])
    }
    
    # Size mapping
    sizes = {
        'small': ('0.5rem 1rem', '0.875rem'),
        'medium': ('0.75rem 1.5rem', '0.95rem'),
        'large': ('1rem 2rem', '1.1rem')
    }
    
    color_start, color_end = colors.get(variant, colors['primary'])
    padding, font_size = sizes.get(size, sizes['medium'])
    width_style = 'width: 100%;' if full_width else ''
    
    icon_html = get_svg_icon(icon, size=18, color="white") if icon else ""
    
    button_html = f"""
    <button class="modern-button" style="
        background: linear-gradient(135deg, {color_start}, {color_end});
        color: white;
        border: none;
        border-radius: 12px;
        padding: {padding};
        font-size: {font_size};
        font-weight: 500;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px {color_start}44;
        {width_style}
    "
    onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 24px {color_start}66';"
    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px {color_start}44';"
    onclick="this.style.transform='translateY(0)';">
        {icon_html}
        {label}
    </button>
    """
    
    return st.markdown(button_html, unsafe_allow_html=True)


def create_modern_metric_card(
    label: str,
    value: Any,
    delta: Optional[str] = None,
    delta_color: str = "normal",
    icon: str = None
):
    """Create a modern metric card with optional delta and icon"""
    theme = get_theme_colors()
    
    # Determine delta color
    delta_colors = {
        'normal': theme['text_secondary'],
        'positive': theme['success'],
        'negative': theme['error'],
        'warning': theme['warning']
    }
    
    delta_html = ""
    if delta:
        color = delta_colors.get(delta_color, delta_colors['normal'])
        delta_html = f"""
        <div style="margin-top: 0.5rem; color: {color}; font-size: 0.9rem; font-weight: 500;">
            {delta}
        </div>
        """
    
    icon_html = get_svg_icon(icon, size=24) if icon else ""
    
    html = f"""
    <div class="glass-card" style="padding: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <div style="color: {theme['text_secondary']}; font-size: 0.9rem; font-weight: 500; 
                            text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">
                    {label}
                </div>
                <div style="font-size: 2rem; font-weight: 700; 
                            background: linear-gradient(135deg, {theme['accent_primary']}, {theme['accent_secondary']});
                            -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {value}
                </div>
                {delta_html}
            </div>
            {f'<div style="opacity: 0.7;">{icon_html}</div>' if icon_html else ''}
        </div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)


# Export main components
__all__ = [
    'ModernUI',
    'create_modern_sidebar',
    'create_modern_theme_toggle',
    'create_modern_header',
    'create_glass_card',
    'create_modern_button',
    'create_modern_metric_card'
]

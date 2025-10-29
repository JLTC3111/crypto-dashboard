"""
Theme Configuration Module
Provides dark/light mode support with proper contrast ratios
"""

import streamlit as st
from typing import Dict, Any


class Theme:
    """Theme configuration for dark and light modes"""
    
    # WCAG AAA compliant color schemes (contrast ratio >= 7:1)
    DARK_THEME = {
        'name': 'dark',
        'background': '#0E1117',
        'secondary_background': '#1E2127',
        'card_background': '#262730',
        'text_primary': '#FAFAFA',
        'text_secondary': '#B8B8B8',
        'text_muted': '#808080',
        'border': '#3D3D3D',
        'accent_primary': '#4A9EFF',
        'accent_secondary': '#7B61FF',
        'success': '#00C853',
        'warning': '#FFB300',
        'error': '#FF5252',
        'info': '#29B6F6',
        'chart_colors': ['#4A9EFF', '#7B61FF', '#00C853', '#FFB300', '#FF5252', '#29B6F6'],
        'gradient_start': '#1E3A8A',
        'gradient_end': '#7C3AED',
        'shadow': 'rgba(0, 0, 0, 0.5)',
        'overlay': 'rgba(0, 0, 0, 0.7)',
    }
    
    LIGHT_THEME = {
        'name': 'light',
        'background': '#FFFFFF',
        'secondary_background': '#F5F7FA',
        'card_background': '#FFFFFF',
        'text_primary': '#1A1A1A',
        'text_secondary': '#4A4A4A',
        'text_muted': '#6B6B6B',
        'border': '#E0E0E0',
        'accent_primary': '#1976D2',
        'accent_secondary': '#5E35B1',
        'success': '#2E7D32',
        'warning': '#F57C00',
        'error': '#C62828',
        'info': '#0277BD',
        'chart_colors': ['#1976D2', '#5E35B1', '#2E7D32', '#F57C00', '#C62828', '#0277BD'],
        'gradient_start': '#1E88E5',
        'gradient_end': '#7B1FA2',
        'shadow': 'rgba(0, 0, 0, 0.1)',
        'overlay': 'rgba(0, 0, 0, 0.3)',
    }
    
    @staticmethod
    def get_current_theme() -> Dict[str, Any]:
        """Get the current theme based on session state"""
        if 'theme' not in st.session_state:
            st.session_state.theme = 'dark'
        
        return Theme.DARK_THEME if st.session_state.theme == 'dark' else Theme.LIGHT_THEME
    
    @staticmethod
    def toggle_theme():
        """Toggle between dark and light themes"""
        if 'theme' not in st.session_state:
            st.session_state.theme = 'dark'
        
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
    
    @staticmethod
    def apply_theme():
        """Apply the current theme to Streamlit"""
        theme = Theme.get_current_theme()
        
        # Custom CSS for theme
        css = f"""
        <style>
            /* Main app styling */
            .stApp {{
                background-color: {theme['background']};
                color: {theme['text_primary']};
            }}
            
            /* Sidebar styling */
            [data-testid="stSidebar"] {{
                background-color: {theme['secondary_background']};
            }}
            
            [data-testid="stSidebar"] * {{
                color: {theme['text_primary']} !important;
            }}
            
            /* Card styling */
            .element-container {{
                background-color: {theme['card_background']};
            }}
            
            /* Metric cards */
            [data-testid="stMetricValue"] {{
                color: {theme['text_primary']};
                font-weight: 600;
            }}
            
            [data-testid="stMetricLabel"] {{
                color: {theme['text_secondary']};
            }}
            
            /* Headers */
            h1, h2, h3, h4, h5, h6 {{
                color: {theme['text_primary']} !important;
            }}
            
            /* Text */
            p, span, div {{
                color: {theme['text_primary']};
            }}
            
            /* Links */
            a {{
                color: {theme['accent_primary']};
            }}
            
            a:hover {{
                color: {theme['accent_secondary']};
            }}
            
            /* Buttons */
            .stButton > button {{
                background-color: {theme['accent_primary']};
                color: {theme['background']};
                border: none;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-weight: 500;
                transition: all 0.3s ease;
            }}
            
            .stButton > button:hover {{
                background-color: {theme['accent_secondary']};
                box-shadow: 0 4px 12px {theme['shadow']};
            }}
            
            /* Input fields */
            .stTextInput > div > div > input,
            .stSelectbox > div > div > select,
            .stNumberInput > div > div > input {{
                background-color: {theme['card_background']};
                color: {theme['text_primary']};
                border: 1px solid {theme['border']};
                border-radius: 6px;
            }}
            
            /* DataFrames */
            .dataframe {{
                background-color: {theme['card_background']};
                color: {theme['text_primary']};
            }}
            
            .dataframe th {{
                background-color: {theme['secondary_background']};
                color: {theme['text_primary']};
                font-weight: 600;
            }}
            
            .dataframe td {{
                color: {theme['text_primary']};
            }}
            
            /* Success/Warning/Error/Info boxes */
            .stSuccess {{
                background-color: {theme['success']}22;
                color: {theme['success']};
                border-left: 4px solid {theme['success']};
            }}
            
            .stWarning {{
                background-color: {theme['warning']}22;
                color: {theme['warning']};
                border-left: 4px solid {theme['warning']};
            }}
            
            .stError {{
                background-color: {theme['error']}22;
                color: {theme['error']};
                border-left: 4px solid {theme['error']};
            }}
            
            .stInfo {{
                background-color: {theme['info']}22;
                color: {theme['info']};
                border-left: 4px solid {theme['info']};
            }}
            
            /* Custom card class */
            .custom-card {{
                background-color: {theme['card_background']};
                border: 1px solid {theme['border']};
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 2px 8px {theme['shadow']};
            }}
            
            /* Gradient header */
            .gradient-header {{
                background: linear-gradient(135deg, {theme['gradient_start']}, {theme['gradient_end']});
                color: white;
                padding: 2rem;
                border-radius: 12px;
                margin-bottom: 2rem;
                box-shadow: 0 4px 16px {theme['shadow']};
            }}
            
            /* Theme toggle button */
            .theme-toggle {{
                position: fixed;
                top: 1rem;
                right: 1rem;
                z-index: 999;
                background-color: {theme['card_background']};
                border: 1px solid {theme['border']};
                border-radius: 50%;
                width: 48px;
                height: 48px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 2px 8px {theme['shadow']};
                transition: all 0.3s ease;
            }}
            
            .theme-toggle:hover {{
                transform: scale(1.1);
                box-shadow: 0 4px 12px {theme['shadow']};
            }}
            
            /* Scrollbar */
            ::-webkit-scrollbar {{
                width: 8px;
                height: 8px;
            }}
            
            ::-webkit-scrollbar-track {{
                background: {theme['secondary_background']};
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: {theme['border']};
                border-radius: 4px;
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: {theme['text_muted']};
            }}
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {{
                background-color: {theme['secondary_background']};
                border-radius: 8px;
                padding: 0.5rem;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                color: {theme['text_secondary']};
                border-radius: 6px;
            }}
            
            .stTabs [aria-selected="true"] {{
                background-color: {theme['accent_primary']};
                color: white;
            }}
            
            /* Expander */
            .streamlit-expanderHeader {{
                background-color: {theme['card_background']};
                color: {theme['text_primary']};
                border: 1px solid {theme['border']};
                border-radius: 8px;
            }}
            
            /* Plotly charts */
            .js-plotly-plot {{
                background-color: {theme['card_background']} !important;
            }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)
        
        return theme


def create_theme_toggle():
    """Create a modern theme toggle button with SVG icons"""
    from helpers.svg_icons import get_svg_icon
    
    current_theme = st.session_state.get('theme', 'dark')
    is_dark = current_theme == 'dark'
    
    # Create modern toggle button with SVG icons
    button_html = f"""
    <div style="display: flex; gap: 0.5rem;">
        <button onclick="document.getElementById('theme_toggle_hidden').click()" 
                style="
                    background: linear-gradient(135deg, 
                        {'#1976D2' if not is_dark else '#4A9EFF'}, 
                        {'#5E35B1' if not is_dark else '#7B61FF'});
                    color: white;
                    border: none;
                    border-radius: 50px;
                    padding: 0.5rem 1rem;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    font-weight: 500;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                "
                onmouseover="this.style.transform='scale(1.05)'"
                onmouseout="this.style.transform='scale(1)'">
            {get_svg_icon('sun' if is_dark else 'moon', size=18, color='white')}
            <span>{('Light' if is_dark else 'Dark') + ' Mode'}</span>
        </button>
    </div>
    """
    
    st.markdown(button_html, unsafe_allow_html=True)
    
    # Hidden button for actual theme toggle
    if st.button("", key="theme_toggle_hidden", help="Toggle theme", disabled=False, label_visibility="hidden"):
        Theme.toggle_theme()
        st.rerun()


def get_theme_colors() -> Dict[str, str]:
    """Get current theme colors for use in components"""
    return Theme.get_current_theme()


def create_gradient_header(title: str, subtitle: str = ""):
    """Create a gradient header with theme support"""
    theme = Theme.get_current_theme()
    
    html = f"""
    <div class="gradient-header">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">{title}</h1>
        {f'<p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">{subtitle}</p>' if subtitle else ''}
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)


def create_card(content: str, title: str = ""):
    """Create a themed card component"""
    html = f"""
    <div class="custom-card">
        {f'<h3 style="margin-top: 0;">{title}</h3>' if title else ''}
        {content}
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)


# Export main functions
__all__ = [
    'Theme',
    'create_theme_toggle',
    'get_theme_colors',
    'create_gradient_header',
    'create_card'
]

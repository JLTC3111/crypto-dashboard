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
                isolation: isolate; /* Create new stacking context */
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
                z-index: -999; /* Way behind everything */
                will-change: opacity;
            }}
            
            /* Ensure main content stays above background */
            .main .block-container {{
                position: relative;
                z-index: 10; /* Higher z-index for content */
            }}
            
            /* Ensure all streamlit elements are visible and above background */
            section.main > div {{
                position: relative;
                z-index: 10;
            }}
            
            [data-testid="stAppViewContainer"] {{
                position: relative;
                z-index: 10;
            }}
            
            /* Force all interactive elements above background */
            [data-testid="stAppViewContainer"] > div {{
                position: relative;
                z-index: 10;
            }}
            
            /* Ensure all streamlit widgets are clickable */
            .stButton, .stSelectbox, .stSlider, .stCheckbox, 
            .stTextInput, .stNumberInput, .stDataFrame {{
                position: relative;
                z-index: 100; /* Widgets on top */
            }}
            
            /* Modern Sidebar Design - Optimized */
            [data-testid="stSidebar"] {{
                background: linear-gradient(135deg, {theme['secondary_background']}ee, {theme['card_background']}dd);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border-right: 1px solid {theme['border']}44;
                box-shadow: 4px 0 24px {theme['shadow']};
                position: relative;
                z-index: 999; /* Sidebar should be on top */
            }}
            
            /* Ensure sidebar content is interactive */
            [data-testid="stSidebar"] > div {{
                position: relative;
                z-index: 1000;
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
                z-index: 100; /* Ensure buttons are clickable */
                isolation: isolate; /* Create new stacking context for pseudo-elements */
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
                z-index: -1; /* Behind button content but within button context */
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
                z-index: 10; /* Above background */
                isolation: isolate; /* Create stacking context */
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
                z-index: -1; /* Behind card content but within card */
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
                z-index: 10; /* Above background */
                isolation: isolate; /* Create stacking context */
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
                pointer-events: none;
                z-index: -1; /* Behind header content but within header */
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
                position: relative;
                z-index: 10; /* Above background */
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
            
            /* Additional z-index fixes for all content containers */
            [data-testid="stVerticalBlock"] {{
                position: relative;
                z-index: 10;
            }}
            
            [data-testid="stHorizontalBlock"] {{
                position: relative;
                z-index: 10;
            }}
            
            [data-testid="column"] {{
                position: relative;
                z-index: 10;
            }}
            
            /* Ensure markdown content is visible */
            [data-testid="stMarkdownContainer"] {{
                position: relative;
                z-index: 10;
            }}
            
            /* Fix for any absolute/fixed positioned elements */
            [data-testid="stHeader"] {{
                z-index: 1000;
            }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)


def create_modern_sidebar():
    """Create a simplified modern sidebar without settings (settings moved to main content)"""
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
        
        # Navigation info or additional content can go here
        st.markdown("""
        <div style="text-align: center; padding: 1rem; opacity: 0.6;">
            <p style="font-size: 0.8rem; margin: 0;">
                Navigate using the pages on the left.<br>
                Settings are available on the right side.
            </p>
        </div>
        """, unsafe_allow_html=True)


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


def create_settings_panel():
    """Create a modern settings panel for the right side of the page"""
    theme = get_theme_colors()
    
    # Settings Panel Header
    settings_header = f"""
    <div class="glass-card" style="margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
            {get_svg_icon('settings', size=24)}
            <h2 style="margin: 0; font-weight: 600; font-size: 1.5rem;">{t('settings')}</h2>
        </div>
    """
    st.markdown(settings_header, unsafe_allow_html=True)
    
    # Language Section (without duplicate label)
    lang_section = f"""
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem;">
                {get_svg_icon('language', size=20)}
                <span style="font-weight: 500; font-size: 1rem;">{t('language')}</span>
            </div>
        </div>
    """
    st.markdown(lang_section, unsafe_allow_html=True)
    
    # Language selector without label (to avoid duplication)
    from helpers.i18n import I18n
    languages = I18n.get_available_languages()
    current_lang = I18n.get_current_language()
    
    lang_codes = list(languages.keys())
    current_index = lang_codes.index(current_lang) if current_lang in lang_codes else 0
    
    selected_lang = st.selectbox(
        "Select language",  # Hidden label
        options=lang_codes,
        format_func=lambda x: f"{languages[x]} ({x.upper()})",
        index=current_index,
        key='settings_panel_language',
        label_visibility="collapsed"  # Hide the label
    )
    
    if selected_lang != current_lang:
        I18n.set_language(selected_lang)
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Theme Section (without duplicate label)
    current_theme = st.session_state.get('theme', 'dark')
    theme_section = f"""
        <div style="margin-bottom: 0.75rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem;">
                {get_svg_icon('sun' if current_theme == 'light' else 'moon', size=20)}
                <span style="font-weight: 500; font-size: 1rem;">{t('theme')}</span>
            </div>
        </div>
    """
    st.markdown(theme_section, unsafe_allow_html=True)
    
    # Theme toggle buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            "☀️ Light",
            use_container_width=True,
            key="theme_light_panel",
            type="primary" if current_theme == 'light' else "secondary"
        ):
            from helpers.theme_config import Theme
            if current_theme != 'light':
                Theme.toggle_theme()
                st.rerun()
    
    with col2:
        if st.button(
            "🌙 Dark",
            use_container_width=True,
            key="theme_dark_panel",
            type="primary" if current_theme == 'dark' else "secondary"
        ):
            from helpers.theme_config import Theme
            if current_theme != 'dark':
                Theme.toggle_theme()
                st.rerun()
    
    # Close the glass card
    st.markdown('</div>', unsafe_allow_html=True)


def apply_light_mode_fix():
    """Apply CSS fix for text visibility in light mode"""
    current_theme = st.session_state.get('theme', 'dark')
    
    if current_theme == 'light':
        st.markdown("""
        <style>
            /* Force dark text for light mode visibility */
            .stMarkdown, .stMarkdown *,
            p, span, div,
            label, label *,
            .glass-card, .glass-card *,
            div[data-baseweb="select"], 
            div[data-baseweb="select"] *,
            label[data-baseweb="checkbox"],
            .stSelectbox label, 
            .stCheckbox label,
            h1, h2, h3, h4, h5, h6 {
                color: #1a1a1a !important;
            }
            
            /* Override any gradient text effects in light mode - AGGRESSIVE */
            h1[style*="background-clip"],
            h2[style*="background-clip"],
            h3[style*="background-clip"],
            h4[style*="background-clip"],
            h5[style*="background-clip"],
            h6[style*="background-clip"],
            span[style*="background-clip"],
            div[style*="background-clip"],
            p[style*="background-clip"],
            h1[style*="webkit-background-clip"],
            h2[style*="webkit-background-clip"],
            h3[style*="webkit-background-clip"],
            span[style*="webkit-background-clip"],
            div[style*="webkit-background-clip"] {
                -webkit-text-fill-color: #000000 !important;
                -webkit-background-clip: unset !important;
                background-clip: unset !important;
                background: none !important;
                color: #000000 !important;
            }
            
            /* Target gradient text wrappers */
            .gradient-text,
            [class*="gradient"] {
                -webkit-text-fill-color: #000000 !important;
                -webkit-background-clip: unset !important;
                background-clip: unset !important;
                background: none !important;
                color: #000000 !important;
            }
            
            /* Make selectboxes taller and more readable with light background */
            div[data-baseweb="select"] > div {
                min-height: 50px !important;
                font-size: 1.1rem !important;
                padding: 0.75rem 1rem !important;
                background-color: #ffffff !important;
                border: 1px solid #d0d0d0 !important;
                color: #1a1a1a !important;
            }
            
            /* Style the selectbox text - dark text on light background */
            div[data-baseweb="select"] > div > div {
                font-size: 1.1rem !important;
                font-weight: 500 !important;
                line-height: 1.5 !important;
                color: #1a1a1a !important;
            }
            
            /* Target all nested text elements within selectbox */
            div[data-baseweb="select"] > div > div > div,
            div[data-baseweb="select"] span,
            div[data-baseweb="select"] p {
                color: #1a1a1a !important;
            }
            
            /* ===== NUCLEAR OPTION: POPOVER DROPDOWN MENU ===== */
            
            /* Target the popover container that holds the dropdown */
            [data-baseweb="popover"],
            div[data-baseweb="popover"] {
                background-color: #ffffff !important;
                border: 1px solid #d0d0d0 !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
            }
            
            /* Force all children of popover to have dark text */
            [data-baseweb="popover"] *,
            div[data-baseweb="popover"] * {
                color: #000000 !important;
            }
            
            /* Style the dropdown listbox container - AGGRESSIVE TARGETING */
            div[role="listbox"],
            ul[role="listbox"],
            div[data-baseweb="popover"] div[role="listbox"],
            div[data-baseweb="menu"] {
                background-color: #ffffff !important;
                border: 1px solid #d0d0d0 !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
            }
            
            /* Target ALL possible dropdown option selectors - INCLUDING BARE li[role="option"] */
            li[role="option"],
            div[role="listbox"] div[role="option"],
            div[role="listbox"] li[role="option"],
            ul[role="listbox"] li[role="option"],
            div[data-baseweb="menu"] li,
            div[data-baseweb="menu"] div[role="option"],
            li[data-baseweb="list-item"],
            [data-baseweb="popover"] li[role="option"] {
                min-height: 48px !important;
                font-size: 1.05rem !important;
                padding: 0.75rem 1rem !important;
                display: flex !important;
                align-items: center !important;
                background-color: #ffffff !important;
                color: #000000 !important;
            }
            
            /* Target ALL text elements within dropdown options - NUCLEAR */
            li[role="option"] *,
            div[role="listbox"] div[role="option"] *,
            div[role="listbox"] li[role="option"] *,
            ul[role="listbox"] li[role="option"] *,
            div[data-baseweb="menu"] li *,
            div[data-baseweb="menu"] div[role="option"] *,
            li[data-baseweb="list-item"] *,
            [data-baseweb="popover"] li[role="option"] *,
            div[role="listbox"] span,
            div[role="listbox"] div,
            div[role="listbox"] p {
                color: #000000 !important;
                background-color: transparent !important;
            }
            
            /* Hover state for dropdown options - ALL variants INCLUDING BARE */
            li[role="option"]:hover,
            div[role="listbox"] div[role="option"]:hover,
            div[role="listbox"] li[role="option"]:hover,
            ul[role="listbox"] li[role="option"]:hover,
            div[data-baseweb="menu"] li:hover,
            div[data-baseweb="menu"] div[role="option"]:hover,
            li[data-baseweb="list-item"]:hover,
            [data-baseweb="popover"] li[role="option"]:hover {
                background-color: #f5f5f5 !important;
                color: #000000 !important;
            }
            
            /* Hover state text */
            li[role="option"]:hover *,
            div[role="listbox"] div[role="option"]:hover *,
            div[role="listbox"] li[role="option"]:hover *,
            ul[role="listbox"] li[role="option"]:hover *,
            div[data-baseweb="menu"] li:hover *,
            div[data-baseweb="menu"] div[role="option"]:hover *,
            li[data-baseweb="list-item"]:hover *,
            [data-baseweb="popover"] li[role="option"]:hover * {
                color: #000000 !important;
            }
            
            /* Selected/highlighted option - ALL variants INCLUDING BARE */
            li[role="option"][aria-selected="true"],
            div[role="listbox"] div[role="option"][aria-selected="true"],
            div[role="listbox"] li[role="option"][aria-selected="true"],
            ul[role="listbox"] li[role="option"][aria-selected="true"],
            div[data-baseweb="menu"] li[aria-selected="true"],
            div[data-baseweb="menu"] div[role="option"][aria-selected="true"],
            li[data-baseweb="list-item"][aria-selected="true"],
            [data-baseweb="popover"] li[role="option"][aria-selected="true"] {
                background-color: #e3f2fd !important;
                color: #000000 !important;
            }
            
            /* Selected option text */
            li[role="option"][aria-selected="true"] *,
            div[role="listbox"] div[role="option"][aria-selected="true"] *,
            div[role="listbox"] li[role="option"][aria-selected="true"] *,
            ul[role="listbox"] li[role="option"][aria-selected="true"] *,
            div[data-baseweb="menu"] li[aria-selected="true"] *,
            div[data-baseweb="menu"] div[role="option"][aria-selected="true"] *,
            li[data-baseweb="list-item"][aria-selected="true"] *,
            [data-baseweb="popover"] li[role="option"][aria-selected="true"] * {
                color: #000000 !important;
            }
            
            /* Make checkbox labels bigger */
            label[data-baseweb="checkbox"] {
                font-size: 1.05rem !important;
                font-weight: 500 !important;
            }
            
            /* Style checkbox container */
            div[data-testid="stCheckbox"] {
                padding: 0.5rem 0 !important;
            }
            
            /* Make label text more visible */
            .stSelectbox label, .stCheckbox label {
                font-size: 1rem !important;
                font-weight: 600 !important;
                margin-bottom: 0.5rem !important;
            }
            
            /* ===== COMPREHENSIVE TABLE/DATAFRAME STYLING FOR LIGHT MODE - NUCLEAR OPTION ===== */
            
            /* CSS ANIMATION HACK - Force recalculation to override inline styles */
            @keyframes forceBlackText {
                from { color: #000000; }
                to { color: #000000; }
            }
            
            /* ABSOLUTE NUCLEAR: Use filter to invert colors if needed */
            div[data-testid="stDataFrame"],
            div[data-testid="stTable"] {
                /* Uncomment below if all else fails - will invert the entire table */
                /* filter: invert(1) hue-rotate(180deg); */
            }
            
            /* MAXIMUM SPECIFICITY: Force ALL text to black */
            html body div[data-testid="stDataFrame"] *,
            html body div[data-testid="stDataFrame"] td,
            html body div[data-testid="stDataFrame"] th,
            html body div[data-testid="stDataFrame"] div,
            html body div[data-testid="stDataFrame"] span,
            html body div[data-testid="stDataFrame"] p,
            html body div[data-testid="stTable"] *,
            html body div[data-testid="stTable"] td,
            html body div[data-testid="stTable"] th,
            html body div[data-testid="stTable"] div,
            html body div[data-testid="stTable"] span,
            html body div[data-testid="stTable"] p {
                color: #000000 !important;
                -webkit-text-fill-color: #000000 !important;
                text-shadow: none !important;
                animation: forceBlackText 0.01s infinite;
            }
            
            /* Target styled elements specifically */
            html body [data-testid="stDataFrame"] [style*="color"],
            html body [data-testid="stTable"] [style*="color"] {
                color: #000000 !important;
                -webkit-text-fill-color: #000000 !important;
            }
            
            /* Override Streamlit's dataframe container completely */
            div[data-testid="stDataFrame"],
            div[data-testid="stDataFrame"] > div,
            div[data-testid="stDataFrame"] > div > div,
            div[data-testid="stTable"],
            div[data-testid="stTable"] > div,
            div[data-testid="stTable"] > div > div,
            .stDataFrame,
            .stDataFrame > div,
            .stDataFrame > div > div {
                background-color: #ffffff !important;
                background: #ffffff !important;
            }
            
            /* Target all table elements with maximum specificity */
            table,
            table[data-testid],
            .dataframe,
            .stDataFrame table,
            div[data-testid="stDataFrame"] table,
            div[data-testid="stTable"] table {
                background-color: #ffffff !important;
                background: #ffffff !important;
                border: 1px solid #d0d0d0 !important;
            }
            
            /* Table body background */
            tbody,
            table tbody,
            .dataframe tbody,
            .stDataFrame tbody,
            div[data-testid="stDataFrame"] tbody,
            div[data-testid="stTable"] tbody {
                background-color: #ffffff !important;
                background: #ffffff !important;
                color: #000000 !important;
            }
            
            /* Table headers - light gray background with dark text */
            th,
            table th,
            thead th,
            .dataframe th,
            .dataframe thead th,
            .stDataFrame th,
            div[data-testid="stDataFrame"] th,
            div[data-testid="stTable"] th,
            table thead th,
            tbody th {
                background-color: #f8f9fa !important;
                background: #f8f9fa !important;
                color: #000000 !important;
                font-weight: 600 !important;
                border-bottom: 2px solid #d0d0d0 !important;
            }
            
            /* Force all text in headers to be dark */
            th *,
            table th *,
            thead th *,
            .dataframe th *,
            .dataframe thead th *,
            .stDataFrame th *,
            div[data-testid="stDataFrame"] th *,
            div[data-testid="stTable"] th * {
                color: #000000 !important;
            }
            
            /* Table cells - white background with dark text - MAXIMUM SPECIFICITY */
            td,
            td[style],
            table td,
            table td[style],
            tbody td,
            tbody td[style],
            .dataframe td,
            .dataframe tbody td,
            .stDataFrame td,
            div[data-testid="stDataFrame"] td,
            div[data-testid="stTable"] td,
            table tbody td,
            table tbody td[style] {
                background-color: #ffffff !important;
                background: #ffffff !important;
                color: #000000 !important;
                border-bottom: 1px solid #e0e0e0 !important;
            }
            
            /* Override ANY styled td with inline color */
            td[style*="color: green"],
            td[style*="color: red"],
            td[style*="color: white"],
            td[style*="color:green"],
            td[style*="color:red"],
            td[style*="color:white"] {
                color: #000000 !important;
            }
            
            /* Force all text in cells to be dark - OVERRIDE INLINE STYLES */
            td *,
            table td *,
            tbody td *,
            .dataframe td *,
            .dataframe tbody td *,
            .stDataFrame td *,
            div[data-testid="stDataFrame"] td *,
            div[data-testid="stTable"] td *,
            td[style],
            table td[style],
            tbody td[style] {
                color: #000000 !important;
            }
            
            /* Override styled cells with inline styles */
            td[style*="color"],
            table td[style*="color"],
            tbody td[style*="color"],
            .dataframe td[style*="color"],
            .stDataFrame td[style*="color"],
            div[data-testid="stDataFrame"] td[style*="color"],
            td div,
            td span,
            td p,
            table td div,
            table td span,
            table td p,
            tbody td div,
            tbody td span,
            tbody td p {
                color: #000000 !important;
            }
            
            /* Target all child elements with ANY inline style */
            td > *[style],
            table td > *[style],
            tbody td > *[style] {
                color: #000000 !important;
            }
            
            /* Table rows - white background */
            tr,
            table tr,
            tbody tr,
            .dataframe tr,
            .dataframe tbody tr,
            .stDataFrame tr,
            div[data-testid="stDataFrame"] tr,
            div[data-testid="stTable"] tr {
                background-color: #ffffff !important;
                background: #ffffff !important;
                    color: #000000 !important;
            }
            
            /* Hover state for table rows */
            tr:hover,
            tr:hover td,
            table tr:hover,
            table tr:hover td,
            tbody tr:hover,
            tbody tr:hover td,
            .dataframe tr:hover,
            .dataframe tr:hover td,
            .dataframe tbody tr:hover td,
            .stDataFrame tr:hover,
            .stDataFrame tr:hover td,
            div[data-testid="stDataFrame"] tr:hover,
            div[data-testid="stDataFrame"] tr:hover td,
            div[data-testid="stTable"] tr:hover,
            div[data-testid="stTable"] tr:hover td {
                background-color: #f5f5f5 !important;
                background: #f5f5f5 !important;
                color: #000000 !important;
            }
            
            /* Hover state text */
            tr:hover td *,
            table tr:hover td *,
            tbody tr:hover td *,
            .dataframe tr:hover td *,
            .dataframe tbody tr:hover td *,
            .stDataFrame tr:hover td *,
            div[data-testid="stDataFrame"] tr:hover td *,
            div[data-testid="stTable"] tr:hover td * {
                color: #000000 !important;
            }
            
            /* Alternate row colors for better readability */
            tr:nth-child(even),
            tr:nth-child(even) td,
            table tr:nth-child(even),
            table tr:nth-child(even) td,
            tbody tr:nth-child(even),
            tbody tr:nth-child(even) td,
            .dataframe tr:nth-child(even),
            .dataframe tr:nth-child(even) td,
            .dataframe tbody tr:nth-child(even) td,
            .stDataFrame tr:nth-child(even),
            .stDataFrame tr:nth-child(even) td {
                background-color: #fafafa !important;
                background: #fafafa !important;
            }
            
            /* Override any styled components */
            [data-testid="stDataFrame"] [style],
            [data-testid="stTable"] [style] {
                background-color: #ffffff !important;
                background: #ffffff !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            /* Make selectboxes taller and more readable */
            div[data-baseweb="select"] > div {
                min-height: 50px !important;
                font-size: 1.1rem !important;
                padding: 0.75rem 1rem !important;
            }
            
            /* Style the selectbox text */
            div[data-baseweb="select"] > div > div {
                font-size: 1.1rem !important;
                font-weight: 500 !important;
                line-height: 1.5 !important;
            }
            
            /* Style the dropdown options */
            div[role="listbox"] div[role="option"] {
                min-height: 48px !important;
                font-size: 1.05rem !important;
                padding: 0.75rem 1rem !important;
                display: flex !important;
                align-items: center !important;
            }
            
            /* Make checkbox labels bigger */
            label[data-baseweb="checkbox"] {
                font-size: 1.05rem !important;
                font-weight: 500 !important;
            }
            
            /* Style checkbox container */
            div[data-testid="stCheckbox"] {
                padding: 0.5rem 0 !important;
            }
            
            /* Make label text more visible */
            .stSelectbox label, .stCheckbox label {
                font-size: 1rem !important;
                font-weight: 600 !important;
                margin-bottom: 0.5rem !important;
            }
        </style>
        """, unsafe_allow_html=True)


# Export main components
__all__ = [
    'ModernUI',
    'create_modern_sidebar',
    'create_modern_theme_toggle',
    'create_modern_header',
    'create_glass_card',
    'create_modern_button',
    'create_modern_metric_card',
    'create_settings_panel',
    'apply_light_mode_fix'
]

"""
Settings Page
Configure language, theme, and application preferences
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Settings - Crypto Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import helpers with error handling
try:
    from helpers.theme_config import Theme, get_theme_colors
except ImportError:
    Theme = None
    get_theme_colors = None

try:
    from helpers.i18n import I18n, t
except ImportError:
    def t(key):
        translations = {
            'settings': 'Settings',
            'language': 'Language',
            'theme': 'Theme',
            'preferences': 'Preferences',
            'appearance': 'Appearance'
        }
        return translations.get(key, key)

try:
    from helpers.modern_ui import ModernUI, create_modern_header, create_modern_sidebar, apply_light_mode_fix
    from helpers.svg_icons import get_svg_icon
except ImportError as e:
    ModernUI = None
    create_modern_header = None
    create_modern_sidebar = None
    apply_light_mode_fix = None
    def get_svg_icon(name, size=24, color=None):
        return ""

# Apply modern theme
if ModernUI:
    try:
        ModernUI.apply_modern_theme()
    except Exception as e:
        st.error(f"Error applying theme: {e}")
else:
    if Theme:
        Theme.apply_theme()

# Apply light mode text fix
if apply_light_mode_fix:
    apply_light_mode_fix()

# Create sidebar
if create_modern_sidebar:
    try:
        create_modern_sidebar()
    except Exception as e:
        st.sidebar.error(f"Error creating sidebar: {e}")

# Page Header
if create_modern_header:
    try:
        create_modern_header(
            t('settings'),
            "Configure your dashboard preferences",
            icon="settings"
        )
    except Exception as e:
        st.error(f"Error creating header: {e}")
        st.title("⚙️ Settings")
        st.markdown("Configure your dashboard preferences")
else:
    st.title("⚙️ Settings")
    st.markdown("Configure your dashboard preferences")

# Main Settings Layout
col1, col2 = st.columns([1, 1])

with col1:
    # Language Settings Card
    language_card = f"""
    <div class="glass-card" style="margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
            {get_svg_icon('language', size=28)}
            <h2 style="margin: 0; font-weight: 600; font-size: 1.5rem;">{t('language')}</h2>
        </div>
        <p style="opacity: 0.8; margin-bottom: 1.5rem;">
            Select your preferred language for the dashboard interface.
        </p>
    </div>
    """
    st.markdown(language_card, unsafe_allow_html=True)
    
    # Language selector
    try:
        from helpers.i18n import I18n
        languages = I18n.get_available_languages()
        current_lang = I18n.get_current_language()
        
        lang_codes = list(languages.keys())
        current_index = lang_codes.index(current_lang) if current_lang in lang_codes else 0
        
        selected_lang = st.selectbox(
            "Choose Language",
            options=lang_codes,
            format_func=lambda x: f"{languages[x]} ({x.upper()})",
            index=current_index,
            key='settings_page_language',
            help="Select the language for the dashboard interface"
        )
        
        if selected_lang != current_lang:
            I18n.set_language(selected_lang)
            st.success(f"Language changed to {languages[selected_lang]}! 🎉")
            st.rerun()
            
        # Show current language
        st.info(f"📍 Current Language: **{languages[current_lang]} ({current_lang.upper()})**")
        
    except Exception as e:
        st.error(f"Error loading language settings: {e}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Additional Preferences (placeholder for future features)
    preferences_card = f"""
    <div class="glass-card" style="margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
            {get_svg_icon('settings', size=28)}
            <h2 style="margin: 0; font-weight: 600; font-size: 1.5rem;">{t('preferences')}</h2>
        </div>
        <p style="opacity: 0.8; margin-bottom: 1rem;">
            Additional preferences and settings.
        </p>
    </div>
    """
    st.markdown(preferences_card, unsafe_allow_html=True)
    
    # Notification preferences
    enable_notifications = st.checkbox(
        "Enable Notifications",
        value=st.session_state.get('enable_notifications', True),
        help="Receive notifications about price alerts and updates"
    )
    st.session_state['enable_notifications'] = enable_notifications
    
    # Data refresh interval
    refresh_interval = st.selectbox(
        "Data Refresh Interval",
        options=[5, 10, 15, 20, 30],
        index=3,
        format_func=lambda x: f"{x} minutes",
        help="How often to automatically refresh market data"
    )
    st.session_state['refresh_interval'] = refresh_interval

with col2:
    # Theme Settings Card
    current_theme = st.session_state.get('theme', 'dark')
    theme_card = f"""
    <div class="glass-card" style="margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
            {get_svg_icon('sun' if current_theme == 'light' else 'moon', size=28)}
            <h2 style="margin: 0; font-weight: 600; font-size: 1.5rem;">{t('theme')}</h2>
        </div>
        <p style="opacity: 0.8; margin-bottom: 1.5rem;">
            Choose between light and dark mode for comfortable viewing.
        </p>
    </div>
    """
    st.markdown(theme_card, unsafe_allow_html=True)
    
    # Theme selection with preview
    theme_col1, theme_col2 = st.columns(2)
    
    with theme_col1:
        if st.button(
            "☀️ Light Mode",
            use_container_width=True,
            type="primary" if current_theme == 'light' else "secondary",
            help="Switch to light theme"
        ):
            if Theme and current_theme != 'light':
                Theme.toggle_theme()
                st.success("Switched to Light Mode! ☀️")
                st.rerun()
    
    with theme_col2:
        if st.button(
            "🌙 Dark Mode",
            use_container_width=True,
            type="primary" if current_theme == 'dark' else "secondary",
            help="Switch to dark theme"
        ):
            if Theme and current_theme != 'dark':
                Theme.toggle_theme()
                st.success("Switched to Dark Mode! 🌙")
                st.rerun()
    
    # Current theme display
    theme_status = f"""
    <div style="padding: 1rem; background: linear-gradient(135deg, {'#f0f0f0' if current_theme == 'light' else '#1a1a1a'}, 
                 {'#ffffff' if current_theme == 'light' else '#0a0a0a'}); 
                 border-radius: 12px; margin-top: 1rem; text-align: center; border: 2px solid {'#ddd' if current_theme == 'light' else '#333'};">
        <p style="margin: 0; font-weight: 600; font-size: 1.1rem; color: {'#333' if current_theme == 'light' else '#fff'};">
            {'☀️' if current_theme == 'light' else '🌙'} Current Theme: {current_theme.title()} Mode
        </p>
    </div>
    """
    st.markdown(theme_status, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Display Settings (placeholder for future features)
    display_card = f"""
    <div class="glass-card" style="margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
            {get_svg_icon('chart', size=28)}
            <h2 style="margin: 0; font-weight: 600; font-size: 1.5rem;">Display Settings</h2>
        </div>
        <p style="opacity: 0.8; margin-bottom: 1rem;">
            Customize how data is displayed.
        </p>
    </div>
    """
    st.markdown(display_card, unsafe_allow_html=True)
    
    # Currency preference
    currency = st.selectbox(
        "Display Currency",
        options=["USD", "EUR", "GBP", "JPY", "BTC", "ETH"],
        index=0,
        help="Select your preferred currency for displaying prices"
    )
    st.session_state['display_currency'] = currency
    
    # Number formatting
    compact_numbers = st.checkbox(
        "Compact Number Format",
        value=st.session_state.get('compact_numbers', False),
        help="Display large numbers in compact format (e.g., 1.5M instead of 1,500,000)"
    )
    st.session_state['compact_numbers'] = compact_numbers

# Footer info
st.markdown("---")
st.markdown("""
<div style="text-align: center; opacity: 0.6; padding: 2rem 0;">
    <p style="margin: 0;">Settings are automatically saved to your session.</p>
    <p style="margin: 0; font-size: 0.85rem;">Some settings may require a page refresh to take full effect.</p>
</div>
""", unsafe_allow_html=True)

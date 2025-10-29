import streamlit as st

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Crypto Risk Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Crypto Risk Dashboard")
st.markdown("If you see this, Streamlit is working!")

# Test imports one by one
st.subheader("Testing imports...")

# Test theme_config
try:
    from helpers.theme_config import Theme
    st.success("✅ theme_config imported successfully")
    try:
        theme = Theme.apply_theme()
        st.success("✅ Theme applied successfully")
    except Exception as e:
        st.error(f"❌ Error applying theme: {e}")
except ImportError as e:
    st.error(f"❌ Could not import theme_config: {e}")

# Test i18n
try:
    from helpers.i18n import I18n, t
    st.success("✅ i18n imported successfully")
    try:
        test_translation = t('welcome_message')
        st.success(f"✅ Translation test: {test_translation}")
    except Exception as e:
        st.error(f"❌ Error using translation: {e}")
except ImportError as e:
    st.error(f"❌ Could not import i18n: {e}")

# Test modern_ui
try:
    from helpers.modern_ui import ModernUI
    st.success("✅ modern_ui imported successfully")
    try:
        ModernUI.apply_modern_theme()
        st.success("✅ Modern theme applied successfully")
    except Exception as e:
        st.error(f"❌ Error applying modern theme: {e}")
except ImportError as e:
    st.error(f"❌ Could not import modern_ui: {e}")

# Test svg_icons
try:
    from helpers.svg_icons import get_svg_icon
    st.success("✅ svg_icons imported successfully")
    try:
        icon = get_svg_icon('chart')
        st.success(f"✅ SVG icon test successful")
    except Exception as e:
        st.error(f"❌ Error getting SVG icon: {e}")
except ImportError as e:
    st.error(f"❌ Could not import svg_icons: {e}")

st.markdown("---")
st.info("If you see this message, the basic Streamlit app is working. Check the errors above to diagnose import issues.")

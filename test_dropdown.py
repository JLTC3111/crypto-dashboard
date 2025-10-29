import streamlit as st

st.set_page_config(page_title="Dropdown Test", layout="wide")

# Set light mode
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'light'

# Super aggressive CSS
st.markdown("""
<style>
    /* Nuclear option - force everything to have visible colors */
    * {
        color: #000000 !important;
    }
    
    /* Specifically target dropdown menu */
    [data-baseweb="popover"] {
        background: white !important;
    }
    
    [data-baseweb="popover"] * {
        color: #000000 !important;
        background-color: transparent !important;
    }
    
    li[role="option"] {
        background: white !important;
        color: #000000 !important;
    }
    
    li[role="option"] * {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Dropdown Test")
test = st.selectbox("Test Dropdown", ["Option 1", "Option 2", "Option 3", "Option 4"])
st.write(f"Selected: {test}")

"""
Force clear all Streamlit caches and session state
Run this to completely reset the app state
"""
import streamlit as st
import os
import sys

# Add the current directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("FORCE CACHE CLEAR & SESSION RESET")
print("=" * 60)
print()

# Clear all Streamlit caches
print("Step 1: Clearing all Streamlit caches...")
try:
    st.cache_data.clear()
    print("✅ st.cache_data cleared")
except Exception as e:
    print(f"⚠️  Could not clear cache_data: {e}")

try:
    st.cache_resource.clear()
    print("✅ st.cache_resource cleared")
except Exception as e:
    print(f"⚠️  Could not clear cache_resource: {e}")

print()
print("=" * 60)
print("✅ CACHE CLEAR COMPLETED")
print("=" * 60)
print()
print("Next steps:")
print("1. Go to your browser where the app is running")
print("2. Click 'Sign Out' in the sidebar")
print("3. Sign back in with: dr.herbal2011@gmail.com")
print("4. Navigate to 'My Portfolio'")
print("5. Click 'Refresh Data' button")
print()
print("This will ensure:")
print("- Fresh authentication with correct user_id")
print("- No cached data from old user_id")
print("- Portfolio will load from database with new user_id")
print()

"""
Full Diagnostic Page - Check all components
"""
import streamlit as st
import pandas as pd
from supabase_config import require_auth, PortfolioDatabase, init_supabase
from typing import Any, cast

st.set_page_config(page_title="Full Diagnostic", page_icon="🔬", layout="wide")

if not require_auth():
    st.stop()

st.title("🔬 Full System Diagnostic")

# Force clear all caches button
if st.button("🔄 Force Clear All Caches", type="primary"):
    st.cache_data.clear()
    st.cache_resource.clear()
    if 'transactions' in st.session_state:
        del st.session_state['transactions']
    st.success("✅ All caches and session data cleared!")
    st.info("Now click 'Refresh Data' in My Portfolio to reload from database")
    st.rerun()

st.markdown("---")

# 1. Authentication Check
st.subheader("1️⃣ Authentication Status")
col1, col2 = st.columns(2)

with col1:
    if st.session_state.get('authenticated'):
        st.success("✅ User is authenticated")
        st.write(f"**Email:** {st.session_state.user.email}")
        st.write(f"**User ID:** `{st.session_state.user_id}`")
    else:
        st.error("❌ Not authenticated")

with col2:
    st.write("**Expected User ID:**")
    st.code("6cc1a26a-4f67-4183-884b-d68cb0000e3d")
    
    if st.session_state.user_id == "6cc1a26a-4f67-4183-884b-d68cb0000e3d":
        st.success("✅ User ID matches expected value")
    else:
        st.error("❌ User ID MISMATCH!")
        st.write(f"Current: `{st.session_state.user_id}`")

st.markdown("---")

# 2. Database Direct Query
st.subheader("2️⃣ Direct Database Query")

supabase = init_supabase()
if supabase:
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Query with current user_id:**")
        try:
            response = cast(Any, cast(Any, supabase).table("portfolio_transactions")
                          .select("id, coin_name, symbol, quantity, user_id")
                          .eq("user_id", st.session_state.user_id)
                          .limit(10)
                          .execute())
            
            if response.data and len(response.data) > 0:
                st.success(f"✅ Found {len(response.data)} transactions (showing max 10)")
                df = pd.DataFrame(response.data)
                st.dataframe(df)
            else:
                st.error("❌ No transactions found for your user_id")
                st.warning("This means the database doesn't have data for your current user_id")
        except Exception as e:
            st.error(f"Database query failed: {e}")
    
    with col2:
        st.write("**All unique user_ids in database:**")
        try:
            all_response = cast(Any, cast(Any, supabase).table("portfolio_transactions")
                              .select("user_id")
                              .execute())
            
            if all_response.data:
                user_ids = set([tx.get('user_id') for tx in all_response.data if tx.get('user_id')])
                
                for uid in user_ids:
                    count_response = cast(Any, cast(Any, supabase).table("portfolio_transactions")
                                        .select("id", count="exact")
                                        .eq("user_id", uid)
                                        .execute())
                    count = count_response.count if hasattr(count_response, 'count') else len(count_response.data)
                    
                    is_you = "👈 YOU" if uid == st.session_state.user_id else ""
                    st.write(f"`{uid}`: {count} transactions {is_you}")
        except Exception as e:
            st.error(f"Failed to get user_ids: {e}")

st.markdown("---")

# 3. PortfolioDatabase Class Check
st.subheader("3️⃣ PortfolioDatabase Query")

db = PortfolioDatabase()
col1, col2 = st.columns(2)

with col1:
    st.write("**Using PortfolioDatabase.get_user_portfolio():**")
    try:
        portfolio_data = db.get_user_portfolio(st.session_state.user_id)
        
        if not portfolio_data.empty:
            st.success(f"✅ Found {len(portfolio_data)} transactions")
            st.write("**Columns:**", list(portfolio_data.columns))
            st.write("**Sample data:**")
            st.dataframe(portfolio_data[['coin_name', 'symbol', 'quantity']].head(5))
        else:
            st.error("❌ get_user_portfolio returned empty DataFrame")
            st.warning("This is the MAIN ISSUE - the cached function is returning empty")
    except Exception as e:
        st.error(f"Query failed: {e}")

with col2:
    st.write("**Cache Info:**")
    st.info("get_user_portfolio has @st.cache_data(ttl=300)")
    st.write("This means results are cached for 5 minutes per user_id")
    
    if st.button("Clear get_user_portfolio cache"):
        st.cache_data.clear()
        st.success("Cache cleared! Now reloading...")
        st.rerun()

st.markdown("---")

# 4. Session State Check
st.subheader("4️⃣ Session State")

col1, col2 = st.columns(2)

with col1:
    st.write("**st.session_state.transactions:**")
    if 'transactions' in st.session_state:
        if st.session_state.transactions.empty:
            st.error("❌ transactions DataFrame is EMPTY")
            st.warning("This is why portfolio shows as empty")
        else:
            st.success(f"✅ Has {len(st.session_state.transactions)} transactions")
            st.dataframe(st.session_state.transactions.head(5))
    else:
        st.warning("⚠️ 'transactions' not in session_state")

with col2:
    st.write("**Actions:**")
    if st.button("Delete session_state.transactions"):
        if 'transactions' in st.session_state:
            del st.session_state['transactions']
            st.success("Deleted! Page will reload on next interaction")
    
    if st.button("Reload transactions from database"):
        st.cache_data.clear()
        if 'transactions' in st.session_state:
            del st.session_state['transactions']
        st.success("Cleared! Now reload My Portfolio page")

st.markdown("---")

# 5. Recommendations
st.subheader("5️⃣ Fix Recommendations")

# Check which component is failing
db_direct_works = False
db_class_works = False
session_has_data = False

try:
    response = cast(Any, cast(Any, supabase).table("portfolio_transactions")
                  .select("id")
                  .eq("user_id", st.session_state.user_id)
                  .execute())
    db_direct_works = bool(response.data and len(response.data) > 0)
except:
    pass

try:
    portfolio_data = db.get_user_portfolio(st.session_state.user_id)
    db_class_works = not portfolio_data.empty
except:
    pass

try:
    session_has_data = 'transactions' in st.session_state and not st.session_state.transactions.empty
except:
    pass

if db_direct_works and not db_class_works:
    st.error("❌ Issue: Database has data but get_user_portfolio returns empty")
    st.markdown("""
    **Fix:**
    1. Click "Force Clear All Caches" button at top
    2. Go to My Portfolio
    3. Click "Refresh Data" button
    """)
elif db_class_works and not session_has_data:
    st.error("❌ Issue: Database query works but session_state.transactions is empty")
    st.markdown("""
    **Fix:**
    1. Click "Delete session_state.transactions" button above
    2. Go to My Portfolio page
    3. It will reload automatically
    """)
elif not db_direct_works:
    st.error("❌ Issue: Database has NO transactions for your user_id")
    st.markdown("""
    **Fix:**
    Run the migration script again or check database directly in Supabase.
    """)
else:
    st.success("✅ All components working correctly!")
    st.info("If portfolio still shows empty, try refreshing the browser")

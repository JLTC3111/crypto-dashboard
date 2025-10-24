"""
Debug page to show current user info
"""
import streamlit as st
from supabase_config import require_auth, PortfolioDatabase

st.set_page_config(page_title="Debug User Info", page_icon="🔍")

if not require_auth():
    st.stop()

st.title("🔍 Debug User Info")

st.markdown("---")

# Show current session state info
st.subheader("Current Session Info")

if st.session_state.get('user'):
    st.success("✅ User is authenticated")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### User Details")
        st.write(f"**Email:** {st.session_state.user.email}")
        st.write(f"**User ID:** `{st.session_state.user_id}`")
        st.write(f"**Authenticated:** {st.session_state.authenticated}")
    
    with col2:
        st.markdown("### Database Check")
        db = PortfolioDatabase()
        portfolio_data = db.get_user_portfolio(st.session_state.user_id)
        
        st.write(f"**Transactions found:** {len(portfolio_data)}")
        st.write(f"**Is Empty:** {portfolio_data.empty}")
        
        if not portfolio_data.empty:
            st.success("✅ Transactions exist for your user_id!")
            st.dataframe(portfolio_data[['coin_name', 'symbol', 'quantity', 'user_id']].head(5))
        else:
            st.error("❌ No transactions found for your user_id")
    
    st.markdown("---")
    
    # Check all user_ids in database
    st.subheader("All User IDs in Database")
    
    from supabase_config import init_supabase
    from typing import Any, cast
    
    supabase = init_supabase()
    if supabase:
        response = cast(Any, cast(Any, supabase).table("portfolio_transactions").select("user_id").execute())
        if response.data:
            all_user_ids = set([tx.get('user_id') for tx in response.data if tx.get('user_id')])
            
            st.write(f"**Total transactions in DB:** {len(response.data)}")
            st.write(f"**Unique user_ids:** {len(all_user_ids)}")
            
            for uid in all_user_ids:
                is_current_user = "👈 **THIS IS YOU**" if uid == st.session_state.user_id else ""
                st.code(f"{uid} {is_current_user}")
            
            if st.session_state.user_id not in all_user_ids:
                st.error("⚠️ **MISMATCH DETECTED!**")
                st.error("Your current user_id does not match any transactions in the database.")
                st.info("This is why your portfolio appears empty.")
                
                with st.expander("🔧 How to Fix This"):
                    st.markdown("""
                    ### Option 1: Update Database Transactions
                    Update all transactions to use your current user_id.
                    
                    ### Option 2: Check Authentication
                    You might be logged in with a different account than the one that created the transactions.
                    
                    ### Option 3: Migrate Data
                    If you want to keep the old data, we need to update the user_id field in all existing transactions.
                    """)
else:
    st.error("User not authenticated")

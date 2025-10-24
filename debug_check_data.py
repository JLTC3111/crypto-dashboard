"""
Debug script to check user_id in database vs logged in user
"""
import streamlit as st
from supabase import create_client

# Load Supabase credentials
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_ANON_KEY = st.secrets["supabase"]["key"]

# Initialize client
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

print("=== Checking Database User IDs ===")
print()

# Get all transactions (without user filter)
response = supabase.table("portfolio_transactions").select("id, user_id, coin_name, symbol").limit(10).execute()

if response.data:
    print(f"Found {len(response.data)} transactions in database:")
    print()
    
    unique_users = set()
    for tx in response.data:
        user_id = tx.get('user_id', 'NULL')
        unique_users.add(user_id)
        print(f"ID: {tx.get('id')}, User: {user_id}, Coin: {tx.get('coin_name')} ({tx.get('symbol')})")
    
    print()
    print(f"Unique user_ids found: {unique_users}")
    print()
    
    if None in unique_users or 'NULL' in unique_users:
        print("⚠️  WARNING: Some transactions have NULL user_id!")
        print("This means they won't show up for any logged-in user.")
else:
    print("No transactions found in database")

print()
print("=== Current Session Info ===")
print(f"You are logged in as: dr.herbal2011@gmail.com")
print()
print("To see your actual user_id, log into the app and check the sidebar.")
print("Your user_id should match the user_ids in the database for transactions to show.")

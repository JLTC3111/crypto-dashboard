"""
Check current state of database
"""
import streamlit as st
from supabase import create_client
from typing import Any, cast

NEW_USER_ID = "6cc1a26a-4f67-4183-884b-d68cb0000e3d"
OLD_USER_ID = "862b0dff-5f87-4abd-b10b-a0e04c814ce4"

print("=" * 60)
print("CURRENT DATABASE STATE")
print("=" * 60)
print()

# Load Supabase credentials
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_ANON_KEY = st.secrets["supabase"]["key"]

# Initialize client
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Check all user_ids
print("Checking all unique user_ids in database...")
all_response = cast(Any, cast(Any, supabase).table("portfolio_transactions")
                   .select("user_id, coin_name")
                   .execute())

if all_response.data:
    user_ids = {}
    for tx in all_response.data:
        uid = tx.get('user_id')
        if uid not in user_ids:
            user_ids[uid] = 0
        user_ids[uid] += 1
    
    print(f"\nTotal transactions: {len(all_response.data)}")
    print(f"Unique user_ids: {len(user_ids)}")
    print()
    
    for uid, count in user_ids.items():
        marker = ""
        if uid == NEW_USER_ID:
            marker = " ← YOUR CURRENT USER_ID ✅"
        elif uid == OLD_USER_ID:
            marker = " ← OLD USER_ID"
        
        print(f"  {uid}: {count} transactions{marker}")
    
    print()
    
    # Check specifically for new user_id
    new_check = cast(Any, cast(Any, supabase).table("portfolio_transactions")
                    .select("id, coin_name, symbol")
                    .eq("user_id", NEW_USER_ID)
                    .execute())
    
    if new_check.data and len(new_check.data) > 0:
        print("=" * 60)
        print(f"✅ SUCCESS! Found {len(new_check.data)} transactions for your user_id!")
        print("=" * 60)
        print()
        print("Sample transactions for your account:")
        for i, tx in enumerate(new_check.data[:10], 1):
            print(f"  {i}. {tx.get('coin_name')} ({tx.get('symbol')})")
        if len(new_check.data) > 10:
            print(f"  ... and {len(new_check.data) - 10} more")
        
        print()
        print("🎉 Your portfolio should now be visible in the app!")
        print()
        print("Next steps:")
        print("1. Go to your browser with the app open")
        print("2. Refresh the page (Ctrl+R or Cmd+R)")
        print("3. Navigate to 'My Portfolio'")
        print("4. Your transactions should now appear!")
    else:
        print("❌ No transactions found for your current user_id")
        print()
        print("Your user_id:", NEW_USER_ID)
else:
    print("❌ No transactions found in database at all")

print()

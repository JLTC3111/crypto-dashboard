"""
Migration Script: Update all transactions to current user_id (AUTO-CONFIRM)
This will reassign all existing transactions to the currently logged-in user.
"""
import streamlit as st
from supabase import create_client
from typing import Any, cast

# Target user_id (your current logged-in user)
NEW_USER_ID = "6cc1a26a-4f67-4183-884b-d68cb0000e3d"

# Old user_id found in database
OLD_USER_ID = "862b0dff-5f87-4abd-b10b-a0e04c814ce4"

def migrate_transactions():
    """Migrate all transactions to new user_id"""
    
    print("=" * 60)
    print("MIGRATION SCRIPT: Update Transaction User IDs (AUTO)")
    print("=" * 60)
    print()
    
    # Load Supabase credentials
    SUPABASE_URL = st.secrets["supabase"]["url"]
    SUPABASE_ANON_KEY = st.secrets["supabase"]["key"]
    
    # Initialize client
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    
    print(f"Old User ID: {OLD_USER_ID}")
    print(f"New User ID: {NEW_USER_ID}")
    print()
    
    # Step 1: Count transactions with old user_id
    print("Step 1: Checking existing transactions...")
    response = cast(Any, cast(Any, supabase).table("portfolio_transactions")
                    .select("id, coin_name, symbol")
                    .eq("user_id", OLD_USER_ID)
                    .execute())
    
    if not response.data:
        print("❌ No transactions found with old user_id")
        print("Nothing to migrate.")
        return False
    
    transaction_count = len(response.data)
    print(f"✅ Found {transaction_count} transactions to migrate")
    print()
    
    # Show sample of transactions
    print("Sample transactions:")
    for i, tx in enumerate(response.data[:5], 1):
        print(f"  {i}. {tx.get('coin_name')} ({tx.get('symbol')}) - ID: {tx.get('id')}")
    
    if transaction_count > 5:
        print(f"  ... and {transaction_count - 5} more")
    print()
    
    # Auto-confirm
    print("⚠️  AUTO-CONFIRMING: This will update ALL transactions to the new user_id.")
    print()
    
    print("Step 2: Migrating transactions...")
    
    # Step 3: Update all transactions
    try:
        update_response = cast(Any, cast(Any, supabase).table("portfolio_transactions")
                              .update({"user_id": NEW_USER_ID})
                              .eq("user_id", OLD_USER_ID)
                              .execute())
        
        if update_response.data:
            updated_count = len(update_response.data)
            print(f"✅ Successfully updated {updated_count} transactions")
            print()
        else:
            print("⚠️  Update completed (no data returned from API)")
            print()
        
        # Step 4: Verify migration
        print("Step 3: Verifying migration...")
        verify_response = cast(Any, cast(Any, supabase).table("portfolio_transactions")
                               .select("id")
                               .eq("user_id", NEW_USER_ID)
                               .execute())
        
        new_count = len(verify_response.data) if verify_response.data else 0
        print(f"✅ Verified: {new_count} transactions now have new user_id")
        print()
        
        # Check for any remaining old transactions
        old_check = cast(Any, cast(Any, supabase).table("portfolio_transactions")
                        .select("id")
                        .eq("user_id", OLD_USER_ID)
                        .execute())
        
        old_remaining = len(old_check.data) if old_check.data else 0
        
        if old_remaining > 0:
            print(f"⚠️  WARNING: {old_remaining} transactions still have old user_id")
            return False
        else:
            print("✅ No transactions remain with old user_id")
            print()
        
        print("=" * 60)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Refresh your browser (Ctrl+R or Cmd+R)")
        print("2. Click 'Refresh Data' button in My Portfolio")
        print("3. Your transactions should now be visible!")
        print()
        print("If portfolio is still empty:")
        print("- Check the Debug User Info page to verify user_id")
        print("- Make sure you're logged in with: dr.herbal2011@gmail.com")
        print()
        
        return True
        
    except Exception as e:
        print()
        print(f"❌ ERROR during migration: {e}")
        print()
        print("Migration failed. Please check your Supabase connection.")
        return False

if __name__ == "__main__":
    try:
        success = migrate_transactions()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

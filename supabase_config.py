"""
Supabase Configuration and Authentication Module
Handles user authentication and database operations for the Crypto Portfolio Dashboard
"""

import streamlit as st
import os
import re
import base64
import string
import secrets
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import hashlib
import asyncio
import threading
from typing import Callable, Optional, Any, cast

# Supabase Configuration
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_ANON_KEY = st.secrets["supabase"]["key"]

# Initialize Supabase client
@st.cache_resource
def init_supabase() -> Optional[Client]:
    """Initialize and return Supabase client"""
    try:
        if not SUPABASE_URL or not SUPABASE_ANON_KEY:
            st.error("Supabase credentials not found in secrets.toml")
            return None
        
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        
        # Test the connection
        try:
            supabase.table("portfolio_transactions").select("id").limit(1).execute()
        except Exception as test_e:
            st.warning(f"Supabase connection test failed: {test_e}")
        
        return supabase
    except Exception as e:
        st.error(f"Failed to initialize Supabase: {e}")
        return None

# Real-time Subscription Manager
class RealtimeSubscriptionManager:
    """Manages Supabase Realtime subscriptions for portfolio changes"""
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.subscriptions = {}
        self.callbacks = {}
    
    def subscribe_to_portfolio_changes(self, user_id: str, callback: Callable):
        """Subscribe to real-time portfolio changes for a specific user"""
        try:
            # Create a channel for portfolio changes
            channel_name = f"portfolio_changes_{user_id}"
            
            if channel_name not in self.subscriptions:
                # Set up realtime subscription (cast client to Any to satisfy type-checker)
                channel = cast(Any, cast(Any, self.supabase).channel(channel_name))
                
                # Subscribe to INSERT events
                channel.on_postgres_changes(
                    event="INSERT",
                    schema="public",
                    table="portfolio_transactions",
                    filter=f"user_id=eq.{user_id}",
                    callback=self._handle_portfolio_change
                )
                
                # Subscribe to UPDATE events
                channel.on_postgres_changes(
                    event="UPDATE",
                    schema="public",
                    table="portfolio_transactions",
                    filter=f"user_id=eq.{user_id}",
                    callback=self._handle_portfolio_change
                )
                
                # Subscribe to DELETE events
                channel.on_postgres_changes(
                    event="DELETE",
                    schema="public",
                    table="portfolio_transactions",
                    filter=f"user_id=eq.{user_id}",
                    callback=self._handle_portfolio_change
                )
                
                # Subscribe to the channel
                channel.subscribe()
                
                self.subscriptions[channel_name] = channel
                self.callbacks[channel_name] = callback
                
                return True
        except Exception as e:
            st.warning(f"Failed to setup realtime subscription: {e}")
            return False
    
    def _handle_portfolio_change(self, payload):
        """Handle incoming portfolio change events"""
        try:
            # Extract user_id from the payload to find the right callback
            if 'new' in payload and 'user_id' in payload['new']:
                user_id = payload['new']['user_id']
            elif 'old' in payload and 'user_id' in payload['old']:
                user_id = payload['old']['user_id']
            else:
                return
            
            channel_name = f"portfolio_changes_{user_id}"
            if channel_name in self.callbacks:
                # Call the registered callback
                self.callbacks[channel_name](payload)
        except Exception as e:
            st.warning(f"Error handling portfolio change: {e}")
    
    def unsubscribe(self, user_id: str):
        """Unsubscribe from portfolio changes"""
        channel_name = f"portfolio_changes_{user_id}"
        if channel_name in self.subscriptions:
            try:
                self.subscriptions[channel_name].unsubscribe()
                del self.subscriptions[channel_name]
                del self.callbacks[channel_name]
            except Exception as e:
                st.warning(f"Error unsubscribing: {e}")
    
    def cleanup_all(self):
        """Clean up all subscriptions"""
        for channel_name in list(self.subscriptions.keys()):
            try:
                self.subscriptions[channel_name].unsubscribe()
            except:
                pass
        self.subscriptions.clear()
        self.callbacks.clear()

# Authentication Functions
class SupabaseAuth:
    def __init__(self):
        self.supabase = init_supabase()
        self.realtime_manager = RealtimeSubscriptionManager(self.supabase) if self.supabase else None
    
    def sign_up(self, email: str, password: str, full_name: Optional[str] = None):
        """Register a new user"""
        if not self.supabase:
            st.error("Supabase client not initialized")
            return None
            
        try:
            # Prepare user data
            user_data = {}
            if full_name:
                user_data["full_name"] = full_name
            
            # Sign up user
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": user_data
                }
            })
            
            if response.user:
                st.success("✅ Account created successfully! Please check your email to verify your account.")
                return response
            else:
                st.error("❌ Failed to create account. Please try again.")
                return None
                
        except Exception as e:
            error_msg = str(e)
            if "already registered" in error_msg.lower():
                st.error("❌ This email is already registered. Please try signing in instead.")
            elif "password" in error_msg.lower():
                st.error("❌ Password must be at least 6 characters long.")
            else:
                st.error(f"❌ Sign up failed: {error_msg}")
            return None
    
    def sign_in(self, email: str, password: str):
        """Sign in existing user"""
        if not self.supabase:
            st.error("Supabase client not initialized")
            return None
            
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                st.success("✅ Successfully signed in!")
                
                # Check if user needs to change password
                if response.user.user_metadata.get("force_password_change", False):
                    st.warning("🔒 You must change your password before continuing.")
                    st.session_state.force_password_change = True
                    st.session_state.user_for_password_change = response.user
                
                return response
            else:
                st.error("❌ Invalid email or password. Please try again.")
                return None
                
        except Exception as e:
            error_msg = str(e)
            if "invalid" in error_msg.lower() or "credentials" in error_msg.lower():
                st.error("❌ Invalid email or password. Please check your credentials.")
            elif "not confirmed" in error_msg.lower():
                st.error("❌ Please verify your email address before signing in.")
            else:
                st.error(f"❌ Sign in failed: {error_msg}")
            return None
    
    def change_password(self, new_password: str):
        """Change user's password"""
        if not self.supabase:
            st.error("Supabase client not initialized")
            return False
            
        try:
            response = cast(Any, cast(Any, self.supabase).auth.update_user({
                "password": new_password
            }))
            
            if response and getattr(response, 'user', None):
                # Clear force password change flag
                cast(Any, cast(Any, self.supabase).auth.update_user({
                    "data": {
                        "force_password_change": False,
                        "password_changed_at": datetime.now().isoformat()
                    }
                }))
                st.success("✅ Password changed successfully!")
                return True
            else:
                st.error("❌ Failed to change password. Please try again.")
                return False
                
        except Exception as e:
            error_msg = str(e)
            if "password" in error_msg.lower():
                st.error("❌ Password must be at least 6 characters long.")
            else:
                st.error(f"❌ Password change failed: {error_msg}")
            return False
    
    def sign_out(self):
        """Sign out current user"""
        if not self.supabase:
            return False
            
        try:
            self.supabase.auth.sign_out()
            return True
        except Exception as e:
            st.error(f"Sign out failed: {e}")
            return False
    
    def get_current_user(self):
        """Get current authenticated user"""
        try:
            response = cast(Any, cast(Any, self.supabase).auth.get_user())
            return response.user if response else None
        except Exception:
            return None

# Database Operations
class PortfolioDatabase:
    def __init__(self):
        self.supabase = init_supabase()
        self.auth = SupabaseAuth()
    
    def create_tables(self):
        """Create necessary database tables if they don't exist"""
        # This would typically be done via Supabase dashboard or migrations
        # Here we define the table structure for reference
        
        portfolio_table_sql = """
        CREATE TABLE IF NOT EXISTS portfolios (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
            transaction_id VARCHAR(8) UNIQUE NOT NULL,
            coin_name VARCHAR(100) NOT NULL,
            symbol VARCHAR(10) NOT NULL,
            quantity DECIMAL(20, 8) NOT NULL,
            purchase_price DECIMAL(20, 2) NOT NULL,
            current_price DECIMAL(20, 2) DEFAULT 0,
            purchase_date DATE NOT NULL,
            purchase_time TIME NOT NULL,
            target_sell_price DECIMAL(20, 2) DEFAULT 0,
            current_value DECIMAL(20, 2) DEFAULT 0,
            profit_loss DECIMAL(20, 2) DEFAULT 0,
            percentage_change DECIMAL(10, 4) DEFAULT 0,
            coin_id VARCHAR(50) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        CREATE INDEX IF NOT EXISTS idx_portfolios_user_id ON portfolios(user_id);
        CREATE INDEX IF NOT EXISTS idx_portfolios_transaction_id ON portfolios(transaction_id);
        """
        
        return portfolio_table_sql
    
    @st.cache_data(ttl=300)
    def get_user_portfolio(_self, user_id: str) -> pd.DataFrame:
        """Fetch user's portfolio from database"""
        try:
            response = cast(Any, cast(Any, _self.supabase).table("portfolio_transactions").select("*").eq("user_id", user_id).execute())
            if getattr(response, 'data', None):
                return pd.DataFrame(response.data)
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching portfolio: {e}")
            return pd.DataFrame()
    
    def add_transaction(self, user_id: str, transaction_data: dict):
        """Add new transaction to database"""
        try:
            transaction_data['user_id'] = user_id
            transaction_data['created_at'] = datetime.now().isoformat()
            transaction_data['updated_at'] = datetime.now().isoformat()
            
            response = cast(Any, cast(Any, self.supabase).table('portfolio_transactions').insert(transaction_data).execute())
            return response.data[0] if getattr(response, 'data', None) else None
        except Exception as e:
            st.error(f"Failed to add transaction: {e}")
            return None
    
    def update_transaction(self, transaction_id: str, user_id: str, updates: dict):
        """Update existing transaction using its unique transaction_id"""
        try:
            updates['updated_at'] = datetime.now().isoformat()
            response = cast(Any, cast(Any, self.supabase).table('portfolio_transactions').update(updates).eq('transaction_id', transaction_id).eq('user_id', user_id).execute())
            return response.data[0] if getattr(response, 'data', None) else None
        except Exception as e:
            st.error(f"Failed to update transaction: {e}")
            return None
    
    def delete_transaction(self, transaction_id: str, user_id: str):
        """Delete transaction from database using its unique transaction_id"""
        try:
            cast(Any, cast(Any, self.supabase).table('portfolio_transactions').delete().eq('transaction_id', transaction_id).eq('user_id', user_id).execute())
            return True
        except Exception as e:
            st.error(f"Failed to delete transaction: {e}")
            return False
    
    def migrate_add_restructuring_columns(self):
        """Add restructuring columns to the portfolio_transactions table"""
        try:
            # SQL to add the missing restructuring columns
            migration_sql = """
            ALTER TABLE portfolio_transactions 
            ADD COLUMN IF NOT EXISTS transaction_type VARCHAR(20) DEFAULT 'BUY',
            ADD COLUMN IF NOT EXISTS include_in_portfolio BOOLEAN DEFAULT TRUE,
            ADD COLUMN IF NOT EXISTS restructure_group VARCHAR(50),
            ADD COLUMN IF NOT EXISTS adjusted_purchase_price DECIMAL(20, 8),
            ADD COLUMN IF NOT EXISTS original_purchase_price DECIMAL(20, 8),
            ADD COLUMN IF NOT EXISTS cost_basis_transferred DECIMAL(20, 8) DEFAULT 0;
            """
            
            # Execute the migration
            cast(Any, cast(Any, self.supabase).rpc('exec_sql', {'sql': migration_sql}).execute())
            return True
        except Exception as e:
            st.error(f"Migration failed: {e}")
            return False
    
    def fix_null_restructure_groups(self, user_id: str):
        """Update NULL restructure_group values for restructuring transactions"""
        try:
            from datetime import datetime
            
            # Get all restructuring transactions with NULL restructure_group
            response = cast(Any, cast(Any, self.supabase)
                .table('portfolio_transactions')
                .select('transaction_id, transaction_type')
                .eq('user_id', user_id)
                .in_('transaction_type', ['RESTRUCTURE_IN', 'RESTRUCTURE_OUT'])
                .is_('restructure_group', 'null')
                .execute())
            
            if response.data:
                # Generate a default group ID for orphaned restructuring transactions
                default_group = f"RESTR_LEGACY_{datetime.now().strftime('%Y%m%d')}"
                
                for transaction in response.data:
                    cast(Any, cast(Any, self.supabase)
                        .table('portfolio_transactions')
                        .update({'restructure_group': default_group})
                        .eq('transaction_id', transaction['transaction_id'])
                        .eq('user_id', user_id)
                        .execute())
                
                return len(response.data)
            return 0
        except Exception as e:
            st.error(f"Failed to fix NULL restructure groups: {e}")
            return 0
    
    def get_audit_trail(self, user_id: str, limit: int = 100) -> pd.DataFrame:
        """Get audit trail for user's portfolio changes"""
        try:
            response = cast(Any, cast(Any, self.supabase).table('portfolio_transactions').select('transaction_id, coin_name, symbol, created_at, updated_at').eq('user_id', user_id).order('updated_at', desc=True).limit(limit).execute())
            if getattr(response, 'data', None):
                return pd.DataFrame(response.data)
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Failed to fetch audit trail: {e}")
            return pd.DataFrame()

# Streamlit Authentication Integration
def init_auth_state():
    """Initialize authentication state in Streamlit session"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

def show_auth_form():
    """Display authentication form"""
    auth = SupabaseAuth()
    
    # Check if forced password change is required
    if st.session_state.get('force_password_change', False):
        show_forced_password_change()
        return
    
    # Check if Supabase is properly initialized
    if not auth.supabase:
        st.error("❌ Supabase connection failed. Please check your configuration.")
        st.info("📋 Make sure your secrets.toml file contains valid Supabase credentials.")
        return
    
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: white; margin: 0;">🔐 Authentication Required</h2>
        <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0;">Sign in to access your crypto portfolio</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Sign Up"])
    
    with tab1:
        st.markdown("#### Welcome Back!")
        with st.form("signin_form", clear_on_submit=False):
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                submit = st.form_submit_button("🔑 Sign In", type="primary", use_container_width=True)
            with col2:
                if st.form_submit_button("🔄 Clear Form", use_container_width=True):
                    st.rerun()
            
            if submit:
                if not email or not password:
                    st.error("❌ Please fill in all fields.")
                elif "@" not in email:
                    st.error("❌ Please enter a valid email address.")
                else:
                    with st.spinner("Signing in..."):
                        response = auth.sign_in(email, password)
                        if response and response.user:
                            # Check for forced password change
                            if not st.session_state.get('force_password_change', False):
                                st.session_state.authenticated = True
                                st.session_state.user = response.user
                                st.session_state.user_id = response.user.id
                                st.balloons()
                                st.rerun()
                            # If force_password_change is True, the form will rerun and show password change
    
    with tab2:
        st.markdown("#### Create New Account")
        with st.form("signup_form", clear_on_submit=True):
            new_email = st.text_input("📧 Email Address", key="signup_email", placeholder="your.email@example.com")
            new_password = st.text_input("🔒 Password", type="password", key="signup_password", 
                                       placeholder="Minimum 6 characters", help="Password must be at least 6 characters long")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter your password")
            full_name = st.text_input("👤 Full Name (Optional)", placeholder="Your full name")
            
            submit_signup = st.form_submit_button("📝 Create Account", type="primary", use_container_width=True)
            
            if submit_signup:
                if not new_email or not new_password:
                    st.error("❌ Please fill in email and password fields.")
                elif "@" not in new_email:
                    st.error("❌ Please enter a valid email address.")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters long.")
                elif new_password != confirm_password:
                    st.error("❌ Passwords don't match!")
                else:
                    with st.spinner("Creating account..."):
                        response = auth.sign_up(new_email, new_password, full_name)
                        if response and response.user:
                            st.info("📧 Please check your email and click the verification link to complete registration.")
    
    # Debug information (can be removed in production)
    with st.expander("🔧 Debug Information", expanded=False):
        st.write("**Supabase URL:**", SUPABASE_URL[:50] + "..." if len(SUPABASE_URL) > 50 else SUPABASE_URL)
        st.write("**Supabase Client Status:**", "✅ Connected" if auth.supabase else "❌ Not Connected")
        st.write("**Authentication Status:**", st.session_state.get('authenticated', False))

def show_forced_password_change():
    """Show forced password change form"""
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: white; margin: 0;">🔒 Password Change Required</h2>
        <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0;">Your password must be changed before continuing</p>
    </div>
    """, unsafe_allow_html=True)
    
    user = st.session_state.user_for_password_change
    st.info(f"**Account:** {user.email}")
    st.warning("⚠️ This is a temporary password that must be changed immediately.")
    
    with st.form("forced_password_change"):
        st.subheader("🔐 Set New Password")
        
        new_password = st.text_input("New Password", type="password", help="Must be at least 6 characters")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.form_submit_button("✅ Change Password", type="primary"):
                if new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("❌ Passwords don't match!")
                    elif len(new_password) < 6:
                        st.error("❌ Password must be at least 6 characters long!")
                    else:
                        auth = SupabaseAuth()
                        if auth.change_password(new_password):
                            # Password changed successfully
                            st.session_state.force_password_change = False
                            st.session_state.authenticated = True
                            st.session_state.user = user
                            st.session_state.user_id = user.id
                            
                            # Clean up session state
                            if 'user_for_password_change' in st.session_state:
                                del st.session_state.user_for_password_change
                            
                            st.success("✅ Password changed successfully! Redirecting...")
                            st.balloons()
                            st.rerun()
                else:
                    st.error("❌ Please fill in both password fields!")
        
        with col2:
            if st.form_submit_button("Cancel & Sign Out"):
                # Clear all session state and return to login
                st.session_state.force_password_change = False
                if 'user_for_password_change' in st.session_state:
                    del st.session_state.user_for_password_change
                
                auth = SupabaseAuth()
                auth.sign_out()
                st.info("Signed out. Please sign in again.")
                st.rerun()

def get_svg_icon(icon_name: str, width: int = 24, height: int = 24) -> str:
    """Return inline SVG icon - much more efficient than file loading"""
    
    # Define icons as inline SVG strings
    svg_icons = {
        "user": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
        "logout": f'<svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16,17 21,12 16,7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>'
    }
    
    if icon_name in svg_icons:
        return f'<span style="display: inline-flex; align-items: center; vertical-align: middle; margin-right: 5px;">{svg_icons[icon_name]}</span>'
    else:
        # Fallback to emoji
        fallback_icons = {
            "user": "👤",
            "logout": "🚪"
        }
        return fallback_icons.get(icon_name, "📌")

def show_user_info():
    """Display current user info and logout option"""
    if st.session_state.authenticated and st.session_state.user:
        user_email = st.session_state.user.email
        
        # Display user info with SVG icon using HTML component
        user_icon_html = get_svg_icon("user", width=20, height=20)
        st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            {user_icon_html}
            <strong>Logged in as:</strong> {user_email}
        </div>
        """, unsafe_allow_html=True)
        
        # Sign out button (buttons don't support HTML, so use emoji fallback)
        if st.sidebar.button("Sign Out", key="signout_btn"):
            auth = SupabaseAuth()
            if auth.sign_out():
                st.session_state.authenticated = False
                st.session_state.user = None
                st.session_state.user_id = None
                st.success("Successfully signed out!")
                st.rerun()

def require_auth():
    """Decorator/function to require authentication"""
    init_auth_state()
    
    if not st.session_state.authenticated:
        show_auth_form()
        return False
    
    show_user_info()
    return True

# ==================================================================================================
# ADMIN FUNCTIONS FOR PASSWORD MANAGEMENT
# ==================================================================================================

class SupabaseAdmin:
    """Admin functions for user management using service role key"""
    
    def __init__(self):
        self.supabase_url = SUPABASE_URL
        try:
            self.service_role_key = st.secrets["supabase"]["service_role_key"]
            self.allowed_admins = st.secrets.get("admin", {}).get("allowed_admins", [])
        except KeyError:
            st.error("❌ Service role key not found in secrets. Please add it for admin operations.")
            self.service_role_key = None
            self.allowed_admins = []
        
        # Initialize admin client with service role key
        self.admin_client = None
        if self.service_role_key and self.service_role_key != "YOUR_SERVICE_ROLE_KEY_HERE":
            try:
                self.admin_client = create_client(self.supabase_url, self.service_role_key)
            except Exception as e:
                st.error(f"Failed to initialize admin client: {e}")
    
    def is_admin(self, user_email: str) -> bool:
        """Check if user is an authorized admin"""
        return user_email.lower() in [admin.lower() for admin in self.allowed_admins]
    
    def generate_secure_password(self, length: int = 12) -> str:
        """Generate a secure temporary password"""
        
        # Use a mix of uppercase, lowercase, digits, and some safe special characters
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        
        # Ensure we have at least one of each type
        password = [
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.digits),
            secrets.choice("!@#$%^&*")
        ]
        
        # Fill the rest randomly
        for _ in range(length - 4):
            password.append(secrets.choice(characters))
        
        # Shuffle the password
        secrets.SystemRandom().shuffle(password)
        return ''.join(password)
    
    def reset_user_password(self, user_email: str, admin_user_email: str, reason: str = "") -> dict:
        """Reset a user's password using admin privileges"""
        
        if not self.admin_client:
            return {
                "success": False,
                "error": "Admin client not initialized. Check service role key configuration."
            }
        
        if not self.is_admin(admin_user_email):
            return {
                "success": False,
                "error": f"User {admin_user_email} is not authorized for admin operations."
            }
        
        try:
            # Generate secure temporary password
            temp_password = self.generate_secure_password()
            
            # Get user by email first
            user_response = cast(Any, cast(Any, self.admin_client).auth.admin.list_users())
            target_user = None

            for user in getattr(user_response, 'users', []):
                if getattr(user, 'email', '').lower() == user_email.lower():
                    target_user = user
                    break
            
            if not target_user:
                return {
                    "success": False,
                    "error": f"User with email {user_email} not found."
                }
            
            # Reset password using admin API
            reset_response = cast(Any, cast(Any, self.admin_client).auth.admin.update_user_by_id(
                target_user.id,
                {
                    "password": temp_password,
                    "user_metadata": {
                        "force_password_change": True,
                        "password_reset_by": admin_user_email,
                        "password_reset_at": datetime.now().isoformat(),
                        "reset_reason": reason or "Admin password reset"
                    }
                }
            ))

            if reset_response and getattr(reset_response, 'user', None):
                # Log the admin action
                self._log_admin_action(
                    admin_user_email, 
                    "password_reset", 
                    target_user.id, 
                    user_email, 
                    reason
                )
                
                return {
                    "success": True,
                    "temporary_password": temp_password,
                    "user_id": target_user.id,
                    "message": f"Password reset successful for {user_email}"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to reset password. Supabase API error."
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error during password reset: {str(e)}"
            }
    
    def list_users_for_admin(self, admin_user_email: str) -> dict:
        """List all users for admin management"""
        
        if not self.admin_client:
            return {
                "success": False,
                "error": "Admin client not initialized."
            }
        
        if not self.is_admin(admin_user_email):
            return {
                "success": False,
                "error": "Not authorized for admin operations."
            }
        
        try:
            response = cast(Any, cast(Any, self.admin_client).auth.admin.list_users())
            users_data = []

            for user in getattr(response, 'users', []):
                user_info = {
                    "id": getattr(user, 'id', None),
                    "email": getattr(user, 'email', None),
                    "created_at": getattr(user, 'created_at', None),
                    "last_sign_in_at": getattr(user, 'last_sign_in_at', None),
                    "email_confirmed_at": getattr(user, 'email_confirmed_at', None),
                    "force_password_change": getattr(getattr(user, 'user_metadata', {}), 'get', lambda *_: False)("force_password_change", False) if getattr(user, 'user_metadata', None) else False,
                    "password_reset_by": getattr(getattr(user, 'user_metadata', {}), 'get', lambda *_: "")( "password_reset_by", "" ) if getattr(user, 'user_metadata', None) else "",
                    "password_reset_at": getattr(getattr(user, 'user_metadata', {}), 'get', lambda *_: "")( "password_reset_at", "" ) if getattr(user, 'user_metadata', None) else "",
                }
                users_data.append(user_info)
            
            return {
                "success": True,
                "users": users_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error listing users: {str(e)}"
            }
    
    def force_password_change_flag(self, user_email: str, admin_user_email: str, force: bool = True) -> dict:
        """Set or remove force password change flag for a user"""
        
        if not self.admin_client:
            return {"success": False, "error": "Admin client not initialized."}
        
        if not self.is_admin(admin_user_email):
            return {"success": False, "error": "Not authorized for admin operations."}
        
        try:
            # Get user by email
            user_response = cast(Any, cast(Any, self.admin_client).auth.admin.list_users())
            target_user = None

            for user in getattr(user_response, 'users', []):
                if getattr(user, 'email', '').lower() == user_email.lower():
                    target_user = user
                    break
            
            if not target_user:
                return {"success": False, "error": f"User {user_email} not found."}
            
            # Update user metadata
            update_response = cast(Any, cast(Any, self.admin_client).auth.admin.update_user_by_id(
                target_user.id,
                {
                    "user_metadata": {
                        **(getattr(target_user, 'user_metadata', {}) or {}),
                        "force_password_change": force,
                        "flag_set_by": admin_user_email,
                        "flag_set_at": datetime.now().isoformat()
                    }
                }
            ))

            if update_response and getattr(update_response, 'user', None):
                action = "set" if force else "removed"
                self._log_admin_action(
                    admin_user_email, 
                    f"force_password_change_{action}", 
                    target_user.id, 
                    user_email
                )
                
                return {
                    "success": True,
                    "message": f"Force password change flag {action} for {user_email}"
                }
            else:
                return {"success": False, "error": "Failed to update user metadata."}
                
        except Exception as e:
            return {"success": False, "error": f"Error updating flag: {str(e)}"}
    
    def _log_admin_action(self, admin_email: str, action: str, target_user_id: str, target_email: str, details: str = ""):
        """Log admin actions for audit purposes"""
        try:
            log_entry = {
                "admin_email": admin_email,
                "action": action,
                "target_user_id": target_user_id,
                "target_email": target_email,
                "details": details,
                "timestamp": datetime.now().isoformat(),
                "ip_address": st.session_state.get("user_ip", "unknown")
            }
            
            # Try to insert into admin_audit_log table (guard admin_client for static checkers)
            if self.admin_client:
                cast(Any, cast(Any, self.admin_client).table("admin_audit_log").insert(log_entry).execute())
            else:
                # If admin_client is not available, fallback to logging
                print(f"ADMIN ACTION LOG (no admin_client): {log_entry}")
            
        except Exception as e:
            # Fallback to Streamlit logging if database insert fails
            st.warning(f"Failed to log admin action: {e}")
            print(f"ADMIN ACTION LOG: {log_entry}")

def show_admin_panel():
    """Display admin panel for authorized users"""
    
    if not st.session_state.get('authenticated', False):
        st.error("Please sign in to access admin functions.")
        return
    
    admin = SupabaseAdmin()
    current_user_email = st.session_state.user.email
    
    if not admin.is_admin(current_user_email):
        st.error("❌ You are not authorized to access admin functions.")
        return
    
    st.header("🔧 Admin Panel")
    st.warning("⚠️ Admin functions are powerful and should be used carefully.")
    
    # Create tabs for different admin functions (Password Reset removed - use Quick Reset section instead)
    tab1, tab2 = st.tabs(["� User Management", "📋 Audit Log"])
    
    with tab1:
        st.subheader("👥 User Management")
        
        if st.button("Load Users"):
            result = admin.list_users_for_admin(current_user_email)
            
            if result["success"]:
                users_df = pd.DataFrame(result["users"])
                st.dataframe(users_df, use_container_width=True)
                
                # Force password change controls
                st.subheader("🔒 Password Change Controls")
                selected_email = st.selectbox("Select User", users_df["email"].tolist())
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔐 Force Password Change"):
                        flag_result = admin.force_password_change_flag(str(selected_email), current_user_email, True)
                        if flag_result["success"]:
                            st.success(flag_result["message"])
                        else:
                            st.error(flag_result["error"])
                
                with col2:
                    if st.button("🔓 Remove Force Flag"):
                        flag_result = admin.force_password_change_flag(str(selected_email), current_user_email, False)
                        if flag_result["success"]:
                            st.success(flag_result["message"])
                        else:
                            st.error(flag_result["error"])
            else:
                st.error(f"❌ {result['error']}")
    
    with tab2:
        st.subheader("📋 Admin Audit Log")
        st.info("Audit log functionality requires creating the 'admin_audit_log' table in Supabase.")
        
        # Show SQL to create audit log table
        if st.checkbox("Show SQL for Audit Log Table"):
            st.code("""
CREATE TABLE admin_audit_log (
    id SERIAL PRIMARY KEY,
    admin_email VARCHAR(255) NOT NULL,
    action VARCHAR(100) NOT NULL,
    target_user_id UUID,
    target_email VARCHAR(255),
    details TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address VARCHAR(45)
);

CREATE INDEX idx_admin_audit_admin_email ON admin_audit_log(admin_email);
CREATE INDEX idx_admin_audit_timestamp ON admin_audit_log(timestamp);
CREATE INDEX idx_admin_audit_action ON admin_audit_log(action);
            """, language="sql")

# Export/Import Functions
def export_portfolio_to_excel(df: pd.DataFrame, filename: Optional[str] = None):
    """Export portfolio data to Excel"""
    if filename is None:
        filename = f"crypto_portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    # Create Excel file in memory
    import io
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Portfolio', index=False)
        
        # Get workbook and worksheet (cast to Any to satisfy static type-checker for xlsxwriter workbook)
        workbook = cast(Any, writer.book)
        worksheet = cast(Any, writer.sheets['Portfolio'])
        
        # Add formatting
        money_format = workbook.add_format({'num_format': '$#,##0.00'})
        percent_format = workbook.add_format({'num_format': '0.00%'})
        
        # Apply formatting to relevant columns
        worksheet.set_column('D:F', 15, money_format)  # Price columns
        worksheet.set_column('J:K', 15, money_format)  # Value/P&L columns
        worksheet.set_column('L:L', 15, percent_format)  # Percentage columns
    
    output.seek(0)
    return output.getvalue()

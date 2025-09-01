"""
Admin Panel for Crypto Portfolio Dashboard
Handles password resets and user management for non-existent email addresses
"""

import streamlit as st
from supabase_config import SupabaseAdmin, require_auth, show_admin_panel

# Page configuration
st.set_page_config(
    page_title="Admin Panel",
    page_icon="🔧",
    layout="wide"
)

# Custom CSS for admin styling
st.markdown("""
<style>
    .admin-header {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    .admin-warning {
        background: #ffffff;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #ffc107;
    }
    .admin-success {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #28a745;
    }
    .admin-error {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #dc3545;
    }
    .password-display {
        background: #f8f9fa;
        border: 2px solid #007bff;
        padding: 15px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="admin-header">
    <h1>🔧 Admin Panel</h1>
    <p>Password Reset & User Management System</p>
</div>
""", unsafe_allow_html=True)

# Require authentication
if not st.session_state.get('authenticated', False):
    st.error("❌ Please sign in to access the admin panel.")
    st.info("👈 Use the sidebar to sign in to your account first.")
    st.stop()

# Initialize admin system
admin = SupabaseAdmin()

# Check if user is admin
current_user_email = st.session_state.user.email
if not admin.is_admin(current_user_email):
    st.markdown("""
    <div class="admin-error">
        <h3>❌ Access Denied</h3>
        <p>You are not authorized to access admin functions.</p>
        <p><strong>Your email:</strong> {}</p>
        <p><strong>Authorized admins:</strong> {}</p>
    </div>
    """.format(current_user_email, ", ".join(admin.allowed_admins)), unsafe_allow_html=True)
    st.stop()

# Admin panel content
st.markdown("""
<div class="admin-warning">
    <h4>⚠️ Security Notice</h4>
    <ul>
        <li>Admin functions are powerful and should be used carefully</li>
        <li>All actions are logged for audit purposes</li>
        <li>Service role key must be properly configured</li>
        <li>Temporary passwords should be shared securely (NOT via email)</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Check if admin client is properly configured
if not admin.admin_client:
    st.markdown("""
    <div class="admin-error">
        <h3>❌ Configuration Error</h3>
        <p>Admin client is not properly initialized. Please check:</p>
        <ol>
            <li>Service role key is added to secrets.toml</li>
            <li>Key is not set to "YOUR_SERVICE_ROLE_KEY_HERE"</li>
            <li>Key has proper admin permissions</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Show configuration help
    with st.expander("🔧 Configuration Help"):
        st.markdown("""
        **Step 1: Get your Service Role Key**
        1. Go to your Supabase dashboard
        2. Navigate to Settings → API
        3. Copy the `service_role` key (not the `anon` key)
        
        **Step 2: Update secrets.toml**
        ```toml
        [supabase]
        url = "your_supabase_url"
        key = "your_anon_key"
        service_role_key = "your_service_role_key_here"
        
        [admin]
        allowed_admins = ["admin@example.com", "admin2@example.com"]
        ```
        
        **Step 3: Create Audit Log Table (Optional)**
        Run this SQL in your Supabase SQL editor:
        ```sql
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
        ```
        """)
    st.stop()

# Main admin interface
show_admin_panel()

# Quick reset section for common use case
st.markdown("---")
st.subheader("🚀 Quick Password Reset")
st.info("For users who have accounts with non-existent email addresses and forgot their passwords.")

with st.form("quick_reset_form"):
    st.markdown("### User Information")
    
    col1, col2 = st.columns(2)
    with col1:
        quick_email = st.text_input(
            "User's Email Address",
            placeholder="user@nonexistent-domain.com",
            help="The email address used when the account was created"
        )
    
    with col2:
        quick_reason = st.selectbox(
            "Reason for Reset",
            [
                "User forgot password",
                "Email address doesn't exist",
                "User locked out",
                "Security reset required",
                "Other"
            ]
        )
    
    if quick_reason == "Other":
        custom_reason = st.text_input("Custom Reason", placeholder="Specify reason...")
        final_reason = custom_reason if custom_reason else "Other"
    else:
        final_reason = quick_reason
    
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.form_submit_button("🔄 Reset Password", type="primary"):
            if quick_email:
                with st.spinner("Resetting password..."):
                    result = admin.reset_user_password(quick_email, current_user_email, final_reason)
                
                if result["success"]:
                    st.markdown("""
                    <div class="admin-success">
                        <h4>✅ Password Reset Successful!</h4>
                        <p><strong>User:</strong> {}</p>
                        <p><strong>Reset by:</strong> {}</p>
                    </div>
                    """.format(quick_email, current_user_email), unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div class="password-display">
                        <h4>🔑 Temporary Password</h4>
                        <code>{}</code>
                        <p style="margin-top: 10px; font-size: 14px; font-weight: normal;">
                            ⚠️ Provide this password to the user securely. They will be forced to change it on first login.
                        </p>
                    </div>
                    """.format(result["temporary_password"]), unsafe_allow_html=True)
                    
                    # Instructions for the admin
                    st.markdown("""
                    <div class="admin-warning">
                        <h4>📋 Next Steps</h4>
                        <ol>
                            <li><strong>Copy the temporary password above</strong></li>
                            <li><strong>Contact the user through a secure channel (phone, in-person, secure messaging)</strong></li>
                            <li><strong>Provide them with the temporary password</strong></li>
                            <li><strong>Instruct them to:</strong>
                                <ul>
                                    <li>Go to the login page</li>
                                    <li>Use their email: <code>{}</code></li>
                                    <li>Use the temporary password you provide</li>
                                    <li>They will be prompted to create a new password immediately</li>
                                </ul>
                            </li>
                        </ol>
                    </div>
                    """.format(quick_email), unsafe_allow_html=True)
                    
                else:
                    st.markdown("""
                    <div class="admin-error">
                        <h4>❌ Password Reset Failed</h4>
                        <p><strong>Error:</strong> {}</p>
                    </div>
                    """.format(result["error"]), unsafe_allow_html=True)
            else:
                st.error("Please enter the user's email address.")
    
    with col2:
        st.markdown("""
        **🔒 Security Reminders:**
        - Never send passwords via email
        - Use secure communication channels
        - User will be forced to change password
        - All actions are logged for security
        """)

# Footer with additional info
st.markdown("---")
st.caption("🔐 All admin actions are logged for security and audit purposes. Service role key operations are server-side only.")

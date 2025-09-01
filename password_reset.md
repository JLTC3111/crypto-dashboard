# Admin Password Reset System Guide

## Overview

This system allows authorized administrators to reset passwords for users whose accounts were created with non-existent email addresses. The solution uses Supabase's Admin API with proper security measures.

## 🔧 Setup Instructions

### Step 1: Get Your Service Role Key

1. Go to your Supabase dashboard: https://app.supabase.com
2. Select your project (`idkfmgdfzcs2adrenjcla`)
3. Navigate to **Settings** → **API**
4. Copy the `service_role` key (not the `anon` key)
5. **IMPORTANT**: This key has full admin privileges - keep it secure!

### Step 2: Update Configuration Files

# Admin Configuration
[admin]
# Add your admin email addresses here
allowed_admins = ["your-admin-email@domain.com", "another-admin@domain.com"]
```

### Step 3: Create Audit Log Table (Optional but Recommended)

Run this SQL in your Supabase SQL Editor:

```sql
-- Create admin audit log table
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

-- Create indexes for better performance
CREATE INDEX idx_admin_audit_admin_email ON admin_audit_log(admin_email);
CREATE INDEX idx_admin_audit_timestamp ON admin_audit_log(timestamp);
CREATE INDEX idx_admin_audit_action ON admin_audit_log(action);

-- Enable Row Level Security (RLS)
ALTER TABLE admin_audit_log ENABLE ROW LEVEL SECURITY;

-- Create policy to allow only service role to access
CREATE POLICY "admin_audit_service_role_only" ON admin_audit_log
    USING (auth.role() = 'service_role')
    WITH CHECK (auth.role() = 'service_role');
```

## 🚀 Usage Instructions

### Method 1: Using the Admin Panel (Recommended)

1. **Access the Admin Panel**:
   - Navigate to your app: `/pages/4_Admin_Panel.py`
   - Sign in with an email listed in `allowed_admins`
   - The admin panel will appear automatically

2. **Reset a Password**:
   - Go to the "🚀 Quick Password Reset" section
   - Enter the user's email address
   - Select a reason for the reset
   - Click "🔄 Reset Password"
   - Copy the generated temporary password
   - Provide it to the user securely (NOT via email)

3. **User Experience**:
   - User signs in with their email and the temporary password
   - They are immediately prompted to create a new password
   - They cannot proceed until they change the password
   - Once changed, they have full access to their account

### Method 2: Programmatic Usage

```python
from supabase_config import SupabaseAdmin

# Initialize admin
admin = SupabaseAdmin()

# Reset password
result = admin.reset_user_password(
    user_email="user@nonexistent-domain.com",
    admin_user_email="admin@yourcompany.com",
    reason="User forgot password, email doesn't exist"
)

if result["success"]:
    print(f"Temporary password: {result['temporary_password']}")
    print(f"User ID: {result['user_id']}")
else:
    print(f"Error: {result['error']}")
```

## 🔒 Security Features

### 1. **Service Role Key Protection**
- Never exposed to client-side code
- Only used server-side in admin operations
- Full admin privileges for user management

### 2. **Authorization Control**
- Only emails in `allowed_admins` can perform resets
- Admin status checked before every operation
- Failed authorization attempts are logged

### 3. **Secure Password Generation**
- 12-character passwords with mixed case, numbers, symbols
- Cryptographically secure random generation
- Each password is unique and unpredictable

### 4. **Forced Password Change**
- Users must change temporary passwords immediately
- Cannot access application until password is changed
- Original temporary password becomes invalid after change

### 5. **Audit Logging**
- All admin actions are logged with timestamps
- Includes admin email, target user, and reason
- Stored in secure database table with RLS

### 6. **Session Management**
- Temporary passwords expire after use
- No persistent sessions with temporary credentials
- Proper cleanup of session state

## 📋 Troubleshooting

### Common Issues:

1. **"Admin client not initialized"**
   - Check that `service_role_key` is set in secrets.toml
   - Verify the key is correct (not "YOUR_SERVICE_ROLE_KEY_HERE")
   - Ensure the key has admin permissions

2. **"Not authorized for admin operations"**
   - Add your email to `allowed_admins` in secrets.toml
   - Make sure the email matches exactly (case-sensitive)
   - Restart the Streamlit app after config changes

3. **"User not found"**
   - Verify the email address is correct
   - Check that the user account exists in Supabase Auth
   - User might be using a different email than expected

4. **"Failed to reset password"**
   - Check Supabase service status
   - Verify service role key permissions
   - Look at Supabase logs for detailed error info

### Debug Steps:

1. **Check Configuration**:
   ```python
   from supabase_config import SupabaseAdmin
   admin = SupabaseAdmin()
   print(f"Admin client initialized: {admin.admin_client is not None}")
   print(f"Allowed admins: {admin.allowed_admins}")
   ```

2. **Test Admin Authorization**:
   ```python
   admin = SupabaseAdmin()
   is_admin = admin.is_admin("your-email@domain.com")
   print(f"Is admin: {is_admin}")
   ```

3. **List Users** (for debugging):
   ```python
   admin = SupabaseAdmin()
   result = admin.list_users_for_admin("your-admin-email@domain.com")
   if result["success"]:
       for user in result["users"]:
           print(f"User: {user['email']}, ID: {user['id']}")
   ```

## 🔄 Workflow Example

### Scenario: User "john@fakeemail.com" forgot password

1. **Admin receives request**: User contacts support saying they can't sign in
2. **Verify identity**: Confirm user identity through secure channel
3. **Reset password**: 
   - Admin goes to Admin Panel
   - Enters "john@fakeemail.com"
   - Selects "User forgot password"
   - Clicks "Reset Password"
   - Gets temporary password: "Xy9$mK2pLw8!"
4. **Provide securely**: Admin calls user and provides temporary password
5. **User changes password**:
   - User goes to login page
   - Uses "john@fakeemail.com" and "Xy9$mK2pLw8!"
   - System forces password change
   - User creates new secure password
   - User gains full access to portfolio

## 📊 Admin Panel Features

### Dashboard Tabs:

1. **🔑 Password Reset**: Quick password reset form
2. **👥 User Management**: List users, manage password change flags
3. **📋 Audit Log**: View admin action history (requires audit table)

### User Management Functions:

- **List All Users**: View all registered users with metadata
- **Force Password Change**: Set flag requiring password change on next login
- **Remove Force Flag**: Clear password change requirement
- **View User Details**: See last login, email confirmation status, etc.

## 🎯 Best Practices

### For Admins:

1. **Secure Communication**: Never send passwords via email or insecure channels
2. **Identity Verification**: Always verify user identity before resetting passwords
3. **Document Actions**: Use descriptive reasons for audit trail
4. **Minimal Access**: Only add necessary emails to `allowed_admins`
5. **Regular Review**: Periodically review admin audit logs

### For Security:

1. **Key Management**: Store service role key securely, rotate if compromised
2. **Access Control**: Limit admin panel access to trusted personnel only
3. **Monitoring**: Monitor admin audit logs for suspicious activity
4. **Backup**: Ensure admin credentials and configs are backed up securely

### For Users:

1. **Password Strength**: Encourage strong passwords when changing
2. **Account Recovery**: Provide alternative recovery methods where possible
3. **Documentation**: Keep records of password resets for support tickets

## 🚨 Emergency Procedures

### If Service Role Key is Compromised:

1. **Immediate Action**: Rotate the key in Supabase dashboard
2. **Update Config**: Replace key in secrets.toml immediately
3. **Restart App**: Restart Streamlit application
4. **Audit Review**: Check admin audit logs for unauthorized actions
5. **User Notification**: Consider forcing password changes for all users if needed

### If Admin Account is Compromised:

1. **Remove Access**: Remove email from `allowed_admins`
2. **Review Actions**: Check audit logs for unauthorized admin actions
3. **Reset Affected Users**: Reset passwords for any users that were affected
4. **Restart App**: Restart application to clear any cached permissions

This system provides a secure, auditable way to handle password resets for users with non-existent email addresses while maintaining proper security controls and logging.

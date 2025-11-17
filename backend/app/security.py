import os
import json
from firebase_admin import credentials, initialize_app, auth
from fastapi import Header, HTTPException, Depends

# --- GLOBAL TOGGLE ---
AUTH_ENABLED = os.getenv("AUTH_ENABLED", "true").lower() == "true"
if not AUTH_ENABLED:
    print("⚠️ WARNING: Backend authentication is DISABLED via AUTH_ENABLED=false.")

# Initialize Firebase Admin SDK (only if auth is enabled)
if AUTH_ENABLED:
    try:
        # Load the service account JSON from the environment variable
        service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
        if not service_account_json:
             raise ValueError("FIREBASE_SERVICE_ACCOUNT_JSON not set.")

        cred = credentials.Certificate(json.loads(service_account_json))
        initialize_app(cred)
        print("✅ Firebase Admin SDK initialized.")

    except Exception as e:
        print(f"❌ Firebase Admin SDK Initialization Error: {e}")
        # Force authentication off if initialization fails
        AUTH_ENABLED = False


def get_current_user_id(authorization: str = Header(...)):
    """
    Dependency that validates the Firebase token and returns the user ID.
    """
    if not AUTH_ENABLED:
        # If disabled, skip authentication checks entirely
        return "DEV_USER" 
    
    try:
        # authorization is typically "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
        
        # Verify the token against Firebase
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']
        
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=401, 
            detail="Invalid or expired authentication token."
        )

# Dependency that simply checks if auth is enabled
def require_auth(user_id: str = Depends(get_current_user_id)):
    """
    A simple dependency to ensure the user is authenticated.
    """
    if not AUTH_ENABLED and user_id == "DEV_USER":
        # Allow access if auth is disabled and we're using the dummy user
        return True
    
    # Otherwise, user_id contains the actual Firebase UID
    return True
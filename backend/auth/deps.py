from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.auth.jwt_utils import decode_token

security = HTTPBearer(auto_error=False)

def get_current_username(
    creds: HTTPAuthorizationCredentials | None = Depends(security),
) -> str | None:
    if not creds:
        return None
    username = decode_token(creds.credentials)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username

def require_auth(username: str | None = Depends(get_current_username)) -> str:
    if not username:
        raise HTTPException(status_code=401, detail="Authentication required")
    return username

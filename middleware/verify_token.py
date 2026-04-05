from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from service.supabase_client import get_supabase_client

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    sb = get_supabase_client()
    try:
        res = sb.auth.get_user(credentials.credentials)
        return res.user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

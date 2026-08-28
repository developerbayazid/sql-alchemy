from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.config.config import decode_access_token


async def require_user_id(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = decode_access_token(credentials.credentials)
        return int(payload["user_id"])
        
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")
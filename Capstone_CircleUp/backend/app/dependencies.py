"""
Shared FastAPI dependencies — primarily the get_current_user auth guard.
Protected endpoints return a clean 401, never a raw stack trace.
"""
import logging

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database import get_db
from app.models.user import User
from app.models.token_blacklist import TokenBlacklist

logger = logging.getLogger("circleup")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Resolve the logged-in user from Authorization: Bearer <token>.
    Raises 401 if missing, malformed, expired, or blacklisted.
    """
    if not token:
        raise CREDENTIALS_EXCEPTION

    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise CREDENTIALS_EXCEPTION
    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION

    user_id = payload.get("sub")
    jti = payload.get("jti")
    if user_id is None or jti is None:
        raise CREDENTIALS_EXCEPTION

    is_blacklisted = db.query(TokenBlacklist).filter(TokenBlacklist.jti == jti).first() is not None
    if is_blacklisted:
        raise CREDENTIALS_EXCEPTION

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise CREDENTIALS_EXCEPTION

    return user
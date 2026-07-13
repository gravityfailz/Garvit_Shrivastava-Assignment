
import logging

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.activity_repository import ActivityRepository
from app.repositories.participation_repository import ParticipationRepository

logger = logging.getLogger("circleup")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


# ---- Repository dependencies ----

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_activity_repo(db: Session = Depends(get_db)) -> ActivityRepository:
    return ActivityRepository(db)


def get_participation_repo(db: Session = Depends(get_db)) -> ParticipationRepository:
    return ParticipationRepository(db)


# ---- Auth dependency ----

def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repo),
) -> User:
    """
    Resolve the logged-in user from Authorization: Bearer <token>.
    Returns 401 if the token is missing, invalid, expired, or blacklisted.
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
    jti     = payload.get("jti")
    if user_id is None or jti is None:
        raise CREDENTIALS_EXCEPTION

    if user_repo.is_token_blacklisted(jti):
        raise CREDENTIALS_EXCEPTION

    user = user_repo.get_by_id(int(user_id))
    if user is None:
        raise CREDENTIALS_EXCEPTION

    return user
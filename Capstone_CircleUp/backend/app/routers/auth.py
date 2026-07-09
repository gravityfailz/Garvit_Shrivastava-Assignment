import logging

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.database import get_db
from app.dependencies import get_current_user, oauth2_scheme, CREDENTIALS_EXCEPTION
from app.models.user import User
from app.models.token_blacklist import TokenBlacklist
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.schemas.token import Token

logger = logging.getLogger("circleup")
router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """Create a new account. Email must be unique."""
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists.",
        )
    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        phone_number=payload.phone_number,
        city=payload.city,
        bio=payload.bio,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info("New user registered: user_id=%s email=%s", user.id, user.email)
    return user


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """Validate credentials and return a JWT access token."""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        logger.warning("Failed login attempt for email=%s", payload.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
    token, _jti, _exp = create_access_token(subject=str(user.id))
    logger.info("User logged in: user_id=%s", user.id)
    return Token(access_token=token)


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    token: str | None = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Blacklist the current token — real server-side invalidation."""
    if not token:
        raise CREDENTIALS_EXCEPTION
    try:
        payload = decode_access_token(token)
    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION

    jti = payload.get("jti")
    if not db.query(TokenBlacklist).filter(TokenBlacklist.jti == jti).first():
        db.add(TokenBlacklist(jti=jti))
        db.commit()

    logger.info("User logged out: user_id=%s", current_user.id)
    return {"detail": "Logged out successfully."}
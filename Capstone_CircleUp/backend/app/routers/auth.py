import logging
import jwt
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.dependencies import get_user_repo, oauth2_scheme, CREDENTIALS_EXCEPTION, get_current_user
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.schemas.token import Token

logger = logging.getLogger("circleup")
router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(
    payload: UserCreate,
    user_repo: UserRepository = Depends(get_user_repo),
):
    if user_repo.email_taken(payload.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="An account with this email already exists.")
    user = user_repo.create(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        phone_number=payload.phone_number,
        city=payload.city,
        bio=payload.bio,
    )
    logger.info("New user registered: user_id=%s email=%s", user.id, user.email)
    return user


@router.post("/login", response_model=Token)
def login(
    payload: UserLogin,
    user_repo: UserRepository = Depends(get_user_repo),
):
    user = user_repo.get_by_email(payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        logger.warning("Failed login attempt for email=%s", payload.email)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password.")
    token, _jti, _exp = create_access_token(subject=str(user.id))
    logger.info("User logged in: user_id=%s", user.id)
    return Token(access_token=token)


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    token: str | None = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repo),
):
    if not token:
        raise CREDENTIALS_EXCEPTION
    try:
        payload = decode_access_token(token)
    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION

    jti = payload.get("jti")
    if jti and not user_repo.is_token_blacklisted(jti):
        user_repo.blacklist_token(jti)

    logger.info("User logged out: user_id=%s", current_user.id)
    return {"detail": "Logged out successfully."}
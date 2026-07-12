"""
UserRepository — all database operations for the User model.

Services and routers call these methods instead of writing raw SQLAlchemy
queries inline, separating data-access from business logic.
"""
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.token_blacklist import TokenBlacklist


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---- Reads ----

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def email_taken(self, email: str, exclude_id: int | None = None) -> bool:
        """True if the email is already registered by another user."""
        q = self.db.query(User).filter(User.email == email)
        if exclude_id is not None:
            q = q.filter(User.id != exclude_id)
        return q.first() is not None

    # ---- Writes ----

    def create(
        self,
        *,
        name: str,
        email: str,
        password_hash: str,
        phone_number: str,
        city: str | None,
        bio: str | None,
    ) -> User:
        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            phone_number=phone_number,
            city=city,
            bio=bio,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, updates: dict) -> User:
        for key, value in updates.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    # ---- Token blacklist (auth-related, lives here for convenience) ----

    def is_token_blacklisted(self, jti: str) -> bool:
        return (
            self.db.query(TokenBlacklist)
            .filter(TokenBlacklist.jti == jti)
            .first()
        ) is not None

    def blacklist_token(self, jti: str) -> None:
        self.db.add(TokenBlacklist(jti=jti))
        self.db.commit()
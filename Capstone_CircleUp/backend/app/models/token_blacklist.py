from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class TokenBlacklist(Base):
    """
    Records the `jti` of any JWT that has been explicitly logged out.
    Every authenticated request checks this table via get_current_user.
    """
    __tablename__ = "token_blacklist"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    jti: Mapped[str] = mapped_column(String(36), unique=True, index=True, nullable=False)
    blacklisted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.enums import ParticipationStatus   # ← imported from central enums


class ParticipationRequest(Base):
    __tablename__ = "participation_requests"
    __table_args__ = (
        UniqueConstraint(
            "activity_id", "user_id",
            name="uq_one_request_per_user_per_activity",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[ParticipationStatus] = mapped_column(
        SAEnum(ParticipationStatus, name="participation_status", native_enum=False, length=20),
        nullable=False,
        default=ParticipationStatus.PENDING,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    activity = relationship("Activity", back_populates="participation_requests")
    user = relationship("User", back_populates="participation_requests")
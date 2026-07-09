import enum
from datetime import datetime, date as date_type, time as time_type, timezone
from sqlalchemy import String, Integer, Date, Time, DateTime, ForeignKey
from sqlalchemy import Enum as SAEnum, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class ActivityStatus(str, enum.Enum):
    """
    OPEN and CANCELLED are the only values ever *written* to the DB.
    FULL and COMPLETED are derived lazily at read time — no scheduler needed.
    """
    OPEN = "open"
    FULL = "full"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint("max_participants > 0", name="ck_max_participants_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    location: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    date: Mapped[date_type] = mapped_column(Date, nullable=False, index=True)
    time: Mapped[time_type] = mapped_column(Time, nullable=False)
    max_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[ActivityStatus] = mapped_column(
        SAEnum(ActivityStatus, name="activity_status", native_enum=False, length=20),
        nullable=False,
        default=ActivityStatus.OPEN,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    creator = relationship("User", back_populates="activities")
    participation_requests = relationship(
        "ParticipationRequest", back_populates="activity", cascade="all, delete-orphan"
    )

    @property
    def scheduled_at(self) -> datetime:
        return datetime.combine(self.date, self.time)
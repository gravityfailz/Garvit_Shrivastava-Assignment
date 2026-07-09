"""
Activity status logic (SRS section 7).

`status` column is only ever written as OPEN or CANCELLED.
FULL and COMPLETED are derived here at read time:
  - CANCELLED: sticky regardless of date or capacity.
  - COMPLETED: scheduled date/time is in the past.
  - FULL: approved participants count >= max_participants.
  - Otherwise: OPEN.
"""
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.activity import Activity, ActivityStatus
from app.models.participation import ParticipationRequest, ParticipationStatus
from app.schemas.activity import ActivityOut


def get_approved_participants_count(db: Session, activity_id: int) -> int:
    return (
        db.query(func.count(ParticipationRequest.id))
        .filter(
            ParticipationRequest.activity_id == activity_id,
            ParticipationRequest.status == ParticipationStatus.APPROVED,
        )
        .scalar()
        or 0
    )


def compute_effective_status(activity: Activity, approved_count: int) -> ActivityStatus:
    if activity.status == ActivityStatus.CANCELLED:
        return ActivityStatus.CANCELLED
    if activity.scheduled_at < datetime.now():
        return ActivityStatus.COMPLETED
    if approved_count >= activity.max_participants:
        return ActivityStatus.FULL
    return ActivityStatus.OPEN


def to_activity_out(db: Session, activity: Activity) -> ActivityOut:
    approved_count = get_approved_participants_count(db, activity.id)
    return ActivityOut(
        id=activity.id,
        creator_id=activity.creator_id,
        title=activity.title,
        description=activity.description,
        category=activity.category,
        location=activity.location,
        date=activity.date,
        time=activity.time,
        max_participants=activity.max_participants,
        approved_participants_count=approved_count,
        status=compute_effective_status(activity, approved_count),
        created_at=activity.created_at,
    )
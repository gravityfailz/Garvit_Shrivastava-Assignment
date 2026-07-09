"""Activity status logic (SRS section 7) and serialization helpers."""
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.activity import Activity, ActivityStatus
from app.models.participation import ParticipationRequest, ParticipationStatus
from app.models.user import User
from app.schemas.activity import ActivityOut, ActivityDetailOut


def get_approved_participants_count(db: Session, activity_id: int) -> int:
    return (
        db.query(func.count(ParticipationRequest.id))
        .filter(
            ParticipationRequest.activity_id == activity_id,
            ParticipationRequest.status == ParticipationStatus.APPROVED,
        )
        .scalar() or 0
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


def to_activity_detail_out(
    db: Session, activity: Activity, current_user: User
) -> ActivityDetailOut:
    """
    Build an enriched activity response that includes the current user's
    request status and organizer contact info per SRS sections 7 and 8.
    """
    approved_count = get_approved_participants_count(db, activity.id)
    effective_status = compute_effective_status(activity, approved_count)

    my_request = db.query(ParticipationRequest).filter(
        ParticipationRequest.activity_id == activity.id,
        ParticipationRequest.user_id == current_user.id,
    ).first()

    # SRS 8: organizer phone visible only when the user's request is APPROVED
    organizer_phone = None
    if my_request and my_request.status == ParticipationStatus.APPROVED:
        creator = db.query(User).filter(User.id == activity.creator_id).first()
        if creator:
            organizer_phone = creator.phone_number

    return ActivityDetailOut(
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
        status=effective_status,
        created_at=activity.created_at,
        my_request_id=my_request.id if my_request else None,
        my_request_status=my_request.status if my_request else None,
        organizer_phone=organizer_phone,
    )

from datetime import datetime

from app.models.activity import Activity
from app.models.user import User
from app.enums import ActivityStatus, ParticipationStatus
from app.schemas.activity import ActivityOut, ActivityDetailOut
from app.repositories.participation_repository import ParticipationRepository
from app.repositories.user_repository import UserRepository


def compute_effective_status(activity: Activity, approved_count: int) -> ActivityStatus:
    """Derive the display status — OPEN/CANCELLED are stored; FULL/COMPLETED are derived."""
    if activity.status == ActivityStatus.CANCELLED:
        return ActivityStatus.CANCELLED
    if activity.scheduled_at < datetime.now():
        return ActivityStatus.COMPLETED
    if approved_count >= activity.max_participants:
        return ActivityStatus.FULL
    return ActivityStatus.OPEN


def build_activity_out(activity: Activity, approved_count: int) -> ActivityOut:
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


def resolve_activity_out(
    activity: Activity,
    participation_repo: ParticipationRepository,
) -> ActivityOut:
    approved_count = participation_repo.get_approved_count(activity.id)
    return build_activity_out(activity, approved_count)


def resolve_activity_detail_out(
    activity: Activity,
    current_user: User,
    participation_repo: ParticipationRepository,
    user_repo: UserRepository,
) -> ActivityDetailOut:
   
    approved_count = participation_repo.get_approved_count(activity.id)
    my_request     = participation_repo.get_by_activity_and_user(activity.id, current_user.id)

    organizer_phone = None
    if my_request and my_request.status == ParticipationStatus.APPROVED:
        organizer = user_repo.get_by_id(activity.creator_id)
        if organizer:
            organizer_phone = organizer.phone_number

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
        status=compute_effective_status(activity, approved_count),
        created_at=activity.created_at,
        my_request_id=my_request.id if my_request else None,
        my_request_status=my_request.status if my_request else None,
        organizer_phone=organizer_phone,
    )
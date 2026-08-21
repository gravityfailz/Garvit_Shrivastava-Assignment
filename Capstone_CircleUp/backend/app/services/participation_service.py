
import logging

from fastapi import HTTPException, status

from app.models.user import User
from app.models.participation import ParticipationRequest
from app.enums import ActivityStatus, ParticipationStatus
from app.schemas.participation import ParticipationRequestOut, MyParticipationRequestOut
from app.repositories.activity_repository import ActivityRepository
from app.repositories.participation_repository import ParticipationRepository
from app.repositories.user_repository import UserRepository
from app.services.activity_service import compute_effective_status

logger = logging.getLogger("circleup")


def create_participation_request(
    activity_id: int,
    current_user: User,
    activity_repo: ActivityRepository,
    participation_repo: ParticipationRepository,
) -> ParticipationRequest:
    """SRS 6: validate and create a pending request."""
    activity = activity_repo.get_by_id(activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Activity not found.")

    if activity.creator_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You cannot request to join your own activity.")

    if participation_repo.get_by_activity_and_user(activity_id, current_user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You have already submitted a participation request for this activity.")

    approved_count = participation_repo.get_approved_count(activity_id)
    eff = compute_effective_status(activity, approved_count)

    if eff == ActivityStatus.CANCELLED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This activity has been cancelled.")
    if eff == ActivityStatus.FULL:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This activity is already full.")
    if eff == ActivityStatus.COMPLETED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This activity has already completed.")

    req = participation_repo.create(activity_id, current_user.id)
    logger.info("Request created: request_id=%s activity_id=%s user_id=%s",
                req.id, activity_id, current_user.id)
    return req


def approve_participation_request(
    activity_id: int,
    request_id: int,
    current_user: User,
    activity_repo: ActivityRepository,
    participation_repo: ParticipationRepository,
) -> ParticipationRequest:
    
    activity = activity_repo.get_by_id_with_lock(activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Activity not found.")
    if activity.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only the activity creator can approve requests.")
    if activity.status == ActivityStatus.CANCELLED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cannot approve requests for a cancelled activity.")

    req = participation_repo.get_by_id(request_id)
    if not req or req.activity_id != activity_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Participation request not found.")
    if req.status == ParticipationStatus.APPROVED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This request is already approved.")

    approved_count = participation_repo.get_approved_count(activity_id)
    if approved_count >= activity.max_participants:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot approve: activity is at full capacity ({activity.max_participants} participants).",
        )

    req = participation_repo.update_status(req, ParticipationStatus.APPROVED)
    logger.info("Request approved: request_id=%s activity_id=%s by user_id=%s",
                req.id, activity_id, current_user.id)
    return req


def reject_participation_request(
    activity_id: int,
    request_id: int,
    current_user: User,
    activity_repo: ActivityRepository,
    participation_repo: ParticipationRepository,
) -> ParticipationRequest:
    activity = activity_repo.get_by_id(activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Activity not found.")
    if activity.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only the activity creator can reject requests.")

    req = participation_repo.get_by_id(request_id)
    if not req or req.activity_id != activity_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Participation request not found.")
    if req.status == ParticipationStatus.REJECTED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This request is already rejected.")

    req = participation_repo.update_status(req, ParticipationStatus.REJECTED)
    logger.info("Request rejected: request_id=%s activity_id=%s by user_id=%s",
                req.id, activity_id, current_user.id)
    return req


def get_activity_requests_out(
    activity_id: int,
    current_user: User,
    activity_repo: ActivityRepository,
    participation_repo: ParticipationRepository,
    user_repo: UserRepository,
) -> list[ParticipationRequestOut]:
    activity = activity_repo.get_by_id(activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Activity not found.")
    if activity.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only the activity creator can view participation requests.")

    result = []
    for req in participation_repo.get_by_activity(activity_id):
        user = user_repo.get_by_id(req.user_id)
        result.append(ParticipationRequestOut(
            id=req.id,
            activity_id=req.activity_id,
            user_id=req.user_id,
            status=req.status,
            created_at=req.created_at,
            requester_name=user.name if user else "Unknown",
            requester_phone=(
                user.phone_number
                if (user and req.status == ParticipationStatus.APPROVED)
                else None
            ),
        ))
    return result


def get_my_requests_out(
    current_user: User,
    activity_repo: ActivityRepository,
    participation_repo: ParticipationRepository,
    user_repo: UserRepository,
) -> list[MyParticipationRequestOut]:
    result = []
    for req in participation_repo.get_by_user(current_user.id):
        activity = activity_repo.get_by_id(req.activity_id)
        if not activity:
            continue
        approved_count = participation_repo.get_approved_count(activity.id)
        eff = compute_effective_status(activity, approved_count)
        creator = user_repo.get_by_id(activity.creator_id)
        result.append(MyParticipationRequestOut(
            id=req.id,
            activity_id=req.activity_id,
            status=req.status,
            created_at=req.created_at,
            activity_title=activity.title,
            activity_category=activity.category,
            activity_date=activity.date,
            activity_time=activity.time,
            activity_location=activity.location,
            activity_status=eff,
            organizer_name=creator.name if creator else "Unknown",
            organizer_phone=(
                creator.phone_number
                if (creator and req.status == ParticipationStatus.APPROVED)
                else None
            ),
        ))
    return result
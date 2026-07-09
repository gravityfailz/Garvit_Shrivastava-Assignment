"""
Participation request business logic.

SRS 6: validation rules (own activity, duplicates, cancelled/full).
SRS 7: capacity enforcement with SELECT FOR UPDATE on PostgreSQL.
SRS 8: phone numbers visible only when request is APPROVED.
"""
import logging
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.activity import Activity, ActivityStatus
from app.models.participation import ParticipationRequest, ParticipationStatus
from app.models.user import User
from app.schemas.participation import ParticipationRequestOut, MyParticipationRequestOut
from app.services.activity_service import get_approved_participants_count, compute_effective_status

logger = logging.getLogger("circleup")


def _get_activity_with_lock(db: Session, activity_id: int):
    """
    SELECT FOR UPDATE on PostgreSQL prevents two concurrent approvals from
    both passing the capacity check and over-filling an activity.
    Falls back to a regular SELECT on SQLite (used in tests).
    """
    query = db.query(Activity).filter(Activity.id == activity_id)
    try:
        if hasattr(db, "bind") and db.bind is not None:
            if db.bind.dialect.name == "postgresql":
                query = query.with_for_update()
    except Exception:
        pass
    return query.first()


def create_participation_request(
    db: Session, activity_id: int, current_user: User
) -> ParticipationRequest:
    """SRS 6: Create a pending request, validating all business rules."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found.")

    if activity.creator_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot request to join your own activity.",
        )

    existing = db.query(ParticipationRequest).filter(
        ParticipationRequest.activity_id == activity_id,
        ParticipationRequest.user_id == current_user.id,
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already submitted a participation request for this activity.",
        )

    approved_count = get_approved_participants_count(db, activity_id)
    eff_status = compute_effective_status(activity, approved_count)

    if eff_status == ActivityStatus.CANCELLED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This activity has been cancelled.")
    if eff_status == ActivityStatus.FULL:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This activity is already full.")
    if eff_status == ActivityStatus.COMPLETED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This activity has already completed.")

    req = ParticipationRequest(
        activity_id=activity_id,
        user_id=current_user.id,
        status=ParticipationStatus.PENDING,
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    logger.info("Request created: request_id=%s activity_id=%s user_id=%s",
                req.id, activity_id, current_user.id)
    return req


def approve_participation_request(
    db: Session, activity_id: int, request_id: int, current_user: User
) -> ParticipationRequest:
    """
    SRS 7: Approve with capacity check inside the locked transaction.
    The SELECT FOR UPDATE ensures no two concurrent approvals can both
    pass the check and put the activity over capacity.
    """
    activity = _get_activity_with_lock(db, activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found.")

    if activity.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only the activity creator can approve requests.")

    if activity.status == ActivityStatus.CANCELLED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cannot approve requests for a cancelled activity.")

    req = db.query(ParticipationRequest).filter(
        ParticipationRequest.id == request_id,
        ParticipationRequest.activity_id == activity_id,
    ).first()
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Participation request not found.")
    if req.status == ParticipationStatus.APPROVED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This request is already approved.")

    # Re-count within the locked transaction (SRS 7: cannot exceed capacity)
    approved_count = get_approved_participants_count(db, activity_id)
    if approved_count >= activity.max_participants:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot approve: activity is at full capacity ({activity.max_participants} participants).",
        )

    req.status = ParticipationStatus.APPROVED
    db.commit()
    db.refresh(req)
    logger.info("Request approved: request_id=%s activity_id=%s by user_id=%s",
                req.id, activity_id, current_user.id)
    return req


def reject_participation_request(
    db: Session, activity_id: int, request_id: int, current_user: User
) -> ParticipationRequest:
    """Only the activity creator can reject a request."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found.")

    if activity.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only the activity creator can reject requests.")

    req = db.query(ParticipationRequest).filter(
        ParticipationRequest.id == request_id,
        ParticipationRequest.activity_id == activity_id,
    ).first()
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Participation request not found.")
    if req.status == ParticipationStatus.REJECTED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This request is already rejected.")

    req.status = ParticipationStatus.REJECTED
    db.commit()
    db.refresh(req)
    logger.info("Request rejected: request_id=%s activity_id=%s by user_id=%s",
                req.id, activity_id, current_user.id)
    return req


def get_activity_requests(
    db: Session, activity_id: int, current_user: User
) -> list[ParticipationRequestOut]:
    """
    List all requests for an activity. Only the creator can view these.
    SRS 8: phone number included only for APPROVED participants.
    """
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found.")
    if activity.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only the activity creator can view participation requests.")

    requests = (
        db.query(ParticipationRequest)
        .filter(ParticipationRequest.activity_id == activity_id)
        .order_by(ParticipationRequest.created_at.asc())
        .all()
    )

    result = []
    for req in requests:
        user = db.query(User).filter(User.id == req.user_id).first()
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


def get_my_requests(
    db: Session, current_user: User
) -> list[MyParticipationRequestOut]:
    """
    SRS 9: All requests the current user has submitted across all activities.
    SRS 8: Organizer phone included only for APPROVED requests.
    """
    requests = (
        db.query(ParticipationRequest)
        .filter(ParticipationRequest.user_id == current_user.id)
        .order_by(ParticipationRequest.created_at.desc())
        .all()
    )

    result = []
    for req in requests:
        activity = db.query(Activity).filter(Activity.id == req.activity_id).first()
        if not activity:
            continue
        approved_count = get_approved_participants_count(db, activity.id)
        eff_status = compute_effective_status(activity, approved_count)
        creator = db.query(User).filter(User.id == activity.creator_id).first()
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
            activity_status=eff_status,
            organizer_name=creator.name if creator else "Unknown",
            organizer_phone=(
                creator.phone_number
                if (creator and req.status == ParticipationStatus.APPROVED)
                else None
            ),
        ))
    return result
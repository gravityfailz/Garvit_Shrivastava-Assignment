import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.participation import ParticipationRequestOut
from app.services.participation_service import (
    create_participation_request,
    approve_participation_request,
    reject_participation_request,
    get_activity_requests,
)

logger = logging.getLogger("circleup")
router = APIRouter(prefix="/api/activities", tags=["Participation"])


@router.post(
    "/{activity_id}/requests",
    response_model=ParticipationRequestOut,
    status_code=status.HTTP_201_CREATED,
)
def request_to_join(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Request to join an activity (SRS section 6)."""
    req = create_participation_request(db, activity_id, current_user)
    return ParticipationRequestOut(
        id=req.id,
        activity_id=req.activity_id,
        user_id=req.user_id,
        status=req.status,
        created_at=req.created_at,
        requester_name=current_user.name,
        requester_phone=None,  # pending — not visible yet
    )


@router.get("/{activity_id}/requests", response_model=list[ParticipationRequestOut])
def list_requests(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all participation requests for an activity (owner only). SRS 8."""
    return get_activity_requests(db, activity_id, current_user)


@router.post(
    "/{activity_id}/requests/{request_id}/approve",
    response_model=ParticipationRequestOut,
)
def approve_request(
    activity_id: int,
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Approve a request. SELECT FOR UPDATE on PostgreSQL prevents over-capacity (SRS 7)."""
    req = approve_participation_request(db, activity_id, request_id, current_user)
    requester = db.query(User).filter(User.id == req.user_id).first()
    return ParticipationRequestOut(
        id=req.id,
        activity_id=req.activity_id,
        user_id=req.user_id,
        status=req.status,
        created_at=req.created_at,
        requester_name=requester.name if requester else "",
        requester_phone=requester.phone_number if requester else None,  # approved — visible
    )


@router.post(
    "/{activity_id}/requests/{request_id}/reject",
    response_model=ParticipationRequestOut,
)
def reject_request(
    activity_id: int,
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Reject a participation request (owner only)."""
    req = reject_participation_request(db, activity_id, request_id, current_user)
    requester = db.query(User).filter(User.id == req.user_id).first()
    return ParticipationRequestOut(
        id=req.id,
        activity_id=req.activity_id,
        user_id=req.user_id,
        status=req.status,
        created_at=req.created_at,
        requester_name=requester.name if requester else "",
        requester_phone=None,  # rejected — not visible
    )

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.activity import Activity
from app.models.participation import ParticipationRequest, ParticipationStatus
from app.schemas.user import UserOut, UserUpdate
from app.schemas.activity import ActivityOut
from app.schemas.participation import MyParticipationRequestOut
from app.services.activity_service import to_activity_out
from app.services.participation_service import get_my_requests

logger = logging.getLogger("circleup")
router = APIRouter(prefix="/api/users", tags=["Profile"])


@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """View own profile (SRS section 3)."""
    return current_user


@router.put("/me", response_model=UserOut)
def update_my_profile(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update own profile fields — partial update (SRS section 3)."""
    updates = payload.model_dump(exclude_unset=True)

    if "email" in updates and updates["email"] != current_user.email:
        if db.query(User).filter(
            User.email == updates["email"], User.id != current_user.id
        ).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An account with this email already exists.",
            )

    for field, value in updates.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    logger.info("Profile updated: user_id=%s", current_user.id)
    return current_user


@router.get("/me/activities", response_model=list[ActivityOut])
def get_my_created_activities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """SRS 9: Activities Created — all activities this user has created."""
    activities = (
        db.query(Activity)
        .filter(Activity.creator_id == current_user.id)
        .order_by(Activity.created_at.desc())
        .all()
    )
    return [to_activity_out(db, a) for a in activities]


@router.get("/me/joined", response_model=list[ActivityOut])
def get_my_joined_activities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """SRS 9: Activities Joined — activities where this user has an APPROVED request."""
    approved = (
        db.query(ParticipationRequest)
        .filter(
            ParticipationRequest.user_id == current_user.id,
            ParticipationRequest.status == ParticipationStatus.APPROVED,
        )
        .all()
    )
    ids = [r.activity_id for r in approved]
    activities = db.query(Activity).filter(Activity.id.in_(ids)).all()
    return [to_activity_out(db, a) for a in activities]


@router.get("/me/requests", response_model=list[MyParticipationRequestOut])
def get_my_participation_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """SRS 9: All participation requests the current user has submitted."""
    return get_my_requests(db, current_user)
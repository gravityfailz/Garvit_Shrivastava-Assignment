import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.activity import Activity, ActivityStatus
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityOut
from app.services.activity_service import to_activity_out

logger = logging.getLogger("circleup")
router = APIRouter(prefix="/api/activities", tags=["Activities"])


def _owned_or_error(activity_id: int, current_user: User, db: Session) -> Activity:
    """404 if not found, 403 if found but not owned by current_user."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found.")
    if activity.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this activity.",
        )
    return activity


@router.post("", response_model=ActivityOut, status_code=status.HTTP_201_CREATED)
def create_activity(
    payload: ActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    activity = Activity(
        creator_id=current_user.id,
        title=payload.title,
        description=payload.description,
        category=payload.category,
        location=payload.location,
        date=payload.date,
        time=payload.time,
        max_participants=payload.max_participants,
        status=ActivityStatus.OPEN,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    logger.info("Activity created: activity_id=%s creator_id=%s", activity.id, current_user.id)
    return to_activity_out(db, activity)


@router.get("", response_model=list[ActivityOut])
def list_activities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    activities = db.query(Activity).order_by(Activity.created_at.desc()).all()
    return [to_activity_out(db, a) for a in activities]


@router.get("/{activity_id}", response_model=ActivityOut)
def get_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found.")
    return to_activity_out(db, activity)


@router.put("/{activity_id}", response_model=ActivityOut)
def update_activity(
    activity_id: int,
    payload: ActivityUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    activity = _owned_or_error(activity_id, current_user, db)

    if activity.status == ActivityStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A cancelled activity cannot be edited.",
        )

    updates = payload.model_dump(exclude_unset=True)
    resulting_date = updates.get("date", activity.date)
    resulting_time = updates.get("time", activity.time)

    if datetime.combine(resulting_date, resulting_time) <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity date and time must be in the future.",
        )

    for field, value in updates.items():
        setattr(activity, field, value)

    db.commit()
    db.refresh(activity)
    logger.info("Activity updated: activity_id=%s by user_id=%s", activity.id, current_user.id)
    return to_activity_out(db, activity)


@router.post("/{activity_id}/cancel", response_model=ActivityOut)
def cancel_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    activity = _owned_or_error(activity_id, current_user, db)

    if activity.status == ActivityStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This activity is already cancelled.",
        )

    activity.status = ActivityStatus.CANCELLED
    db.commit()
    db.refresh(activity)
    logger.info("Activity cancelled: activity_id=%s by user_id=%s", activity.id, current_user.id)
    return to_activity_out(db, activity)
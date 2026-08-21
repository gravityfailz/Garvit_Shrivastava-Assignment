import logging
from datetime import datetime, date as date_type
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_current_user, get_activity_repo, get_participation_repo, get_user_repo
from app.models.user import User
from app.enums import ActivityStatus
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityOut, ActivityDetailOut
from app.repositories.activity_repository import ActivityRepository
from app.repositories.participation_repository import ParticipationRepository
from app.repositories.user_repository import UserRepository
from app.services.activity_service import resolve_activity_out, resolve_activity_detail_out

logger = logging.getLogger("circleup")
router = APIRouter(prefix="/api/activities", tags=["Activities"])


def _get_owned_or_error(activity_id, current_user, activity_repo):
    activity = activity_repo.get_by_id(activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Activity not found.")
    if activity.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to modify this activity.")
    return activity


@router.post("", response_model=ActivityOut, status_code=status.HTTP_201_CREATED)
def create_activity(
    payload: ActivityCreate,
    current_user: User = Depends(get_current_user),
    activity_repo: ActivityRepository = Depends(get_activity_repo),
    participation_repo: ParticipationRepository = Depends(get_participation_repo),
):
    activity = activity_repo.create(
        creator_id=current_user.id,
        title=payload.title,
        description=payload.description,
        category=payload.category,
        location=payload.location,
        date=payload.date,
        time=payload.time,
        max_participants=payload.max_participants,
    )
    logger.info("Activity created: activity_id=%s creator_id=%s", activity.id, current_user.id)
    return resolve_activity_out(activity, participation_repo)


@router.get("", response_model=list[ActivityOut])
def list_activities(
    category: str | None = Query(default=None),
    location: str | None = Query(default=None),
    date: date_type | None = Query(default=None),
    sort_by_date: Literal["asc", "desc"] = Query(default="desc"),
    current_user: User = Depends(get_current_user),
    activity_repo: ActivityRepository = Depends(get_activity_repo),
    participation_repo: ParticipationRepository = Depends(get_participation_repo),
):
    activities = activity_repo.get_all(category=category, location=location,
                                       date=date, sort_by_date=sort_by_date)
    return [resolve_activity_out(a, participation_repo) for a in activities]


@router.get("/{activity_id}", response_model=ActivityDetailOut)
def get_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    activity_repo: ActivityRepository = Depends(get_activity_repo),
    participation_repo: ParticipationRepository = Depends(get_participation_repo),
    user_repo: UserRepository = Depends(get_user_repo),
):
    activity = activity_repo.get_by_id(activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Activity not found.")
    return resolve_activity_detail_out(activity, current_user, participation_repo, user_repo)


@router.put("/{activity_id}", response_model=ActivityOut)
def update_activity(
    activity_id: int,
    payload: ActivityUpdate,
    current_user: User = Depends(get_current_user),
    activity_repo: ActivityRepository = Depends(get_activity_repo),
    participation_repo: ParticipationRepository = Depends(get_participation_repo),
):
    activity = _get_owned_or_error(activity_id, current_user, activity_repo)
    if activity.status == ActivityStatus.CANCELLED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="A cancelled activity cannot be edited.")

    updates = payload.model_dump(exclude_unset=True)
    resulting_date = updates.get("date", activity.date)
    resulting_time = updates.get("time", activity.time)
    if datetime.combine(resulting_date, resulting_time) <= datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Activity date and time must be in the future.")

    activity = activity_repo.update(activity, updates)
    logger.info("Activity updated: activity_id=%s by user_id=%s", activity.id, current_user.id)
    return resolve_activity_out(activity, participation_repo)


@router.post("/{activity_id}/cancel", response_model=ActivityOut)
def cancel_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    activity_repo: ActivityRepository = Depends(get_activity_repo),
    participation_repo: ParticipationRepository = Depends(get_participation_repo),
):
    activity = _get_owned_or_error(activity_id, current_user, activity_repo)
    if activity.status == ActivityStatus.CANCELLED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This activity is already cancelled.")

    activity = activity_repo.cancel(activity)
    logger.info("Activity cancelled: activity_id=%s by user_id=%s", activity.id, current_user.id)
    return resolve_activity_out(activity, participation_repo)
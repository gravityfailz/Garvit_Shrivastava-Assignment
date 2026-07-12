import logging
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user, get_user_repo, get_activity_repo, get_participation_repo
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.activity_repository import ActivityRepository
from app.repositories.participation_repository import ParticipationRepository
from app.schemas.user import UserOut, UserUpdate
from app.schemas.activity import ActivityOut
from app.schemas.participation import MyParticipationRequestOut
from app.services.activity_service import resolve_activity_out
from app.services.participation_service import get_my_requests_out

logger = logging.getLogger("circleup")
router = APIRouter(prefix="/api/users", tags=["Profile"])


@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut)
def update_my_profile(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repo),
):
    updates = payload.model_dump(exclude_unset=True)
    if "email" in updates and updates["email"] != current_user.email:
        if user_repo.email_taken(updates["email"], exclude_id=current_user.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="An account with this email already exists.")
    user_repo.update(current_user, updates)
    logger.info("Profile updated: user_id=%s", current_user.id)
    return current_user


@router.get("/me/activities", response_model=list[ActivityOut])
def get_my_created_activities(
    current_user: User = Depends(get_current_user),
    activity_repo: ActivityRepository = Depends(get_activity_repo),
    participation_repo: ParticipationRepository = Depends(get_participation_repo),
):
    activities = activity_repo.get_by_creator(current_user.id)
    return [resolve_activity_out(a, participation_repo) for a in activities]


@router.get("/me/joined", response_model=list[ActivityOut])
def get_my_joined_activities(
    current_user: User = Depends(get_current_user),
    activity_repo: ActivityRepository = Depends(get_activity_repo),
    participation_repo: ParticipationRepository = Depends(get_participation_repo),
):
    ids = participation_repo.get_approved_activity_ids(current_user.id)
    activities = activity_repo.get_by_ids(ids)
    return [resolve_activity_out(a, participation_repo) for a in activities]


@router.get("/me/requests", response_model=list[MyParticipationRequestOut])
def get_my_participation_requests(
    current_user: User = Depends(get_current_user),
    activity_repo: ActivityRepository = Depends(get_activity_repo),
    participation_repo: ParticipationRepository = Depends(get_participation_repo),
    user_repo: UserRepository = Depends(get_user_repo),
):
    return get_my_requests_out(current_user, activity_repo, participation_repo, user_repo)
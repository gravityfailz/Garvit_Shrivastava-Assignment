import logging
from fastapi import APIRouter, Depends, status

from app.dependencies import get_current_user, get_activity_repo, get_participation_repo, get_user_repo
from app.models.user import User
from app.repositories.activity_repository import ActivityRepository
from app.repositories.participation_repository import ParticipationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.participation import ParticipationRequestOut
from app.enums import ParticipationStatus
from app.services.participation_service import (
    create_participation_request,
    approve_participation_request,
    reject_participation_request,
    get_activity_requests_out,
)

logger = logging.getLogger("circleup")
router = APIRouter(prefix="/api/activities", tags=["Participation"])


@router.post("/{activity_id}/requests",
             response_model=ParticipationRequestOut,
             status_code=status.HTTP_201_CREATED)
def request_to_join(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    activity_repo: ActivityRepository = Depends(get_activity_repo),
    participation_repo: ParticipationRepository = Depends(get_participation_repo),
):
    req = create_participation_request(activity_id, current_user,
                                       activity_repo, participation_repo)
    return ParticipationRequestOut(
        id=req.id, activity_id=req.activity_id, user_id=req.user_id,
        status=req.status, created_at=req.created_at,
        requester_name=current_user.name, requester_phone=None,
    )


@router.get("/{activity_id}/requests",
            response_model=list[ParticipationRequestOut])
def list_requests(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    activity_repo: ActivityRepository = Depends(get_activity_repo),
    participation_repo: ParticipationRepository = Depends(get_participation_repo),
    user_repo: UserRepository = Depends(get_user_repo),
):
    return get_activity_requests_out(
        activity_id, current_user, activity_repo, participation_repo, user_repo
    )


@router.post("/{activity_id}/requests/{request_id}/approve",
             response_model=ParticipationRequestOut)
def approve_request(
    activity_id: int,
    request_id: int,
    current_user: User = Depends(get_current_user),
    activity_repo: ActivityRepository = Depends(get_activity_repo),
    participation_repo: ParticipationRepository = Depends(get_participation_repo),
    user_repo: UserRepository = Depends(get_user_repo),
):
    req = approve_participation_request(activity_id, request_id, current_user,
                                        activity_repo, participation_repo)
    requester = user_repo.get_by_id(req.user_id)
    return ParticipationRequestOut(
        id=req.id, activity_id=req.activity_id, user_id=req.user_id,
        status=req.status, created_at=req.created_at,
        requester_name=requester.name if requester else "",
        requester_phone=requester.phone_number if requester else None,
    )


@router.post("/{activity_id}/requests/{request_id}/reject",
             response_model=ParticipationRequestOut)
def reject_request(
    activity_id: int,
    request_id: int,
    current_user: User = Depends(get_current_user),
    activity_repo: ActivityRepository = Depends(get_activity_repo),
    participation_repo: ParticipationRepository = Depends(get_participation_repo),
    user_repo: UserRepository = Depends(get_user_repo),
):
    req = reject_participation_request(activity_id, request_id, current_user,
                                       activity_repo, participation_repo)
    requester = user_repo.get_by_id(req.user_id)
    return ParticipationRequestOut(
        id=req.id, activity_id=req.activity_id, user_id=req.user_id,
        status=req.status, created_at=req.created_at,
        requester_name=requester.name if requester else "",
        requester_phone=None,
    )

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.participation import ParticipationRequest
from app.enums import ParticipationStatus


class ParticipationRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---- Reads ----

    def get_by_id(self, request_id: int) -> ParticipationRequest | None:
        return (
            self.db.query(ParticipationRequest)
            .filter(ParticipationRequest.id == request_id)
            .first()
        )

    def get_by_activity_and_user(
        self, activity_id: int, user_id: int
    ) -> ParticipationRequest | None:
        return (
            self.db.query(ParticipationRequest)
            .filter(
                ParticipationRequest.activity_id == activity_id,
                ParticipationRequest.user_id == user_id,
            )
            .first()
        )

    def get_by_activity(self, activity_id: int) -> list[ParticipationRequest]:
        return (
            self.db.query(ParticipationRequest)
            .filter(ParticipationRequest.activity_id == activity_id)
            .order_by(ParticipationRequest.created_at.asc())
            .all()
        )

    def get_by_user(self, user_id: int) -> list[ParticipationRequest]:
        return (
            self.db.query(ParticipationRequest)
            .filter(ParticipationRequest.user_id == user_id)
            .order_by(ParticipationRequest.created_at.desc())
            .all()
        )

    def get_approved_count(self, activity_id: int) -> int:
        return (
            self.db.query(func.count(ParticipationRequest.id))
            .filter(
                ParticipationRequest.activity_id == activity_id,
                ParticipationRequest.status == ParticipationStatus.APPROVED,
            )
            .scalar()
            or 0
        )

    def get_approved_activity_ids(self, user_id: int) -> list[int]:
        rows = (
            self.db.query(ParticipationRequest.activity_id)
            .filter(
                ParticipationRequest.user_id == user_id,
                ParticipationRequest.status == ParticipationStatus.APPROVED,
            )
            .all()
        )
        return [r[0] for r in rows]

    # ---- Writes ----

    def create(self, activity_id: int, user_id: int) -> ParticipationRequest:
        req = ParticipationRequest(
            activity_id=activity_id,
            user_id=user_id,
            status=ParticipationStatus.PENDING,
        )
        self.db.add(req)
        self.db.commit()
        self.db.refresh(req)
        return req

    def update_status(
        self, request: ParticipationRequest, new_status: ParticipationStatus
    ) -> ParticipationRequest:
        request.status = new_status
        self.db.commit()
        self.db.refresh(request)
        return request
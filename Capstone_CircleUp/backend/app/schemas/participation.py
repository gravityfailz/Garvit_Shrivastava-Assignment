from datetime import datetime, date as date_type, time as time_type
from pydantic import BaseModel

from app.enums import ParticipationStatus, ActivityStatus   # ← from central enums


class ParticipationRequestOut(BaseModel):
    id: int
    activity_id: int
    user_id: int
    status: ParticipationStatus
    created_at: datetime
    requester_name: str = ""
    requester_phone: str | None = None   # SRS 8: only when APPROVED


class MyParticipationRequestOut(BaseModel):
    id: int
    activity_id: int
    status: ParticipationStatus
    created_at: datetime
    activity_title: str
    activity_category: str
    activity_date: date_type
    activity_time: time_type
    activity_location: str
    activity_status: ActivityStatus
    organizer_name: str = ""
    organizer_phone: str | None = None   # SRS 8: only when APPROVED
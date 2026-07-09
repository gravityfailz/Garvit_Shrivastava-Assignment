from datetime import datetime, date as date_type, time as time_type
from pydantic import BaseModel
from app.models.participation import ParticipationStatus
from app.models.activity import ActivityStatus


class ParticipationRequestOut(BaseModel):
    """
    Returned to the activity owner when listing requests.
    SRS 8: requester phone only included when status is APPROVED.
    """
    id: int
    activity_id: int
    user_id: int
    status: ParticipationStatus
    created_at: datetime
    requester_name: str = ""
    requester_phone: str | None = None  # visible only when APPROVED


class MyParticipationRequestOut(BaseModel):
    """
    Returned to the user when they view their own requests.
    SRS 8: organizer phone only included when status is APPROVED.
    """
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
    organizer_phone: str | None = None  # visible only when APPROVED
    
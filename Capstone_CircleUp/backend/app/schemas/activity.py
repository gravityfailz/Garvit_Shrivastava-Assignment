from datetime import date as date_type, time as time_type, datetime
from pydantic import BaseModel, Field, ConfigDict, model_validator

from app.enums import ActivityStatus, ParticipationStatus   # ← from central enums


class ActivityCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    category: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=1, max_length=200)
    date: date_type
    time: time_type
    max_participants: int = Field(gt=0)

    @model_validator(mode="after")
    def check_future_datetime(self):
        scheduled = datetime.combine(self.date, self.time)
        if scheduled <= datetime.now():
            raise ValueError(
                "Activity must be scheduled for a future date and time."
            )
        return self


class ActivityUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    location: str | None = Field(default=None, min_length=1, max_length=200)
    date: date_type | None = None
    time: time_type | None = None
    max_participants: int | None = Field(default=None, gt=0)


class ActivityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    creator_id: int
    title: str
    description: str | None
    category: str
    location: str
    date: date_type
    time: time_type
    max_participants: int
    approved_participants_count: int
    status: ActivityStatus
    created_at: datetime


class ActivityDetailOut(ActivityOut):
    """Extended response with the viewer's request state + contact info (SRS 8)."""
    my_request_id: int | None = None
    my_request_status: ParticipationStatus | None = None
    organizer_phone: str | None = None
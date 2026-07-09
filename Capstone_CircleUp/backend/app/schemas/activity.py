from datetime import date as date_type, time as time_type, datetime
from pydantic import BaseModel, Field, ConfigDict, model_validator
from app.models.activity import ActivityStatus


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
        if datetime.combine(self.date, self.time) <= datetime.now():
            raise ValueError("Activity date and time must be in the future.")
        return self


class ActivityUpdate(BaseModel):
    """All fields optional — partial update semantics."""
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
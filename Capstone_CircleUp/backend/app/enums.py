
import enum


class ActivityStatus(str, enum.Enum):
    """
    OPEN and CANCELLED are the only values written to the database.
    FULL and COMPLETED are derived lazily at read time in activity_service.py.
    """
    OPEN      = "open"
    FULL      = "full"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class ParticipationStatus(str, enum.Enum):
    PENDING  = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
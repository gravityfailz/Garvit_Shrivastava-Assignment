"""
Central enum definitions for CircleUp.

All enums are defined here and imported wherever needed — models, schemas,
services, routers and tests all import from this single source of truth.
"""
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

from datetime import date as date_type
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.enums import ActivityStatus


class ActivityRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---- Reads ----

    def get_by_id(self, activity_id: int) -> Activity | None:
        return self.db.query(Activity).filter(Activity.id == activity_id).first()

    def get_by_id_with_lock(self, activity_id: int) -> Activity | None:
        """
        SELECT FOR UPDATE on PostgreSQL — prevents concurrent over-capacity approvals.
        Falls back to a plain SELECT on SQLite (used in tests).
        """
        query = self.db.query(Activity).filter(Activity.id == activity_id)
        try:
            if hasattr(self.db, "bind") and self.db.bind is not None:
                if self.db.bind.dialect.name == "postgresql":
                    query = query.with_for_update()
        except Exception:
            pass
        return query.first()

    def get_all(
        self,
        category: str | None = None,
        location: str | None = None,
        date: date_type | None = None,
        sort_by_date: str = "desc",
    ) -> list[Activity]:
        query = self.db.query(Activity)
        if category:
            query = query.filter(Activity.category.ilike(f"%{category}%"))
        if location:
            query = query.filter(Activity.location.ilike(f"%{location}%"))
        if date:
            query = query.filter(Activity.date == date)
        if sort_by_date == "asc":
            query = query.order_by(Activity.date.asc(), Activity.time.asc())
        else:
            query = query.order_by(Activity.date.desc(), Activity.time.desc())
        return query.all()

    def get_by_creator(self, creator_id: int) -> list[Activity]:
        return (
            self.db.query(Activity)
            .filter(Activity.creator_id == creator_id)
            .order_by(Activity.created_at.desc())
            .all()
        )

    def get_by_ids(self, ids: list[int]) -> list[Activity]:
        if not ids:
            return []
        return self.db.query(Activity).filter(Activity.id.in_(ids)).all()

    # ---- Writes ----

    def create(
        self,
        *,
        creator_id: int,
        title: str,
        description: str | None,
        category: str,
        location: str,
        date: date_type,
        time,
        max_participants: int,
    ) -> Activity:
        activity = Activity(
            creator_id=creator_id,
            title=title,
            description=description,
            category=category,
            location=location,
            date=date,
            time=time,
            max_participants=max_participants,
            status=ActivityStatus.OPEN,
        )
        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        return activity

    def update(self, activity: Activity, updates: dict) -> Activity:
        for key, value in updates.items():
            setattr(activity, key, value)
        self.db.commit()
        self.db.refresh(activity)
        return activity

    def cancel(self, activity: Activity) -> Activity:
        activity.status = ActivityStatus.CANCELLED
        self.db.commit()
        self.db.refresh(activity)
        return activity
    
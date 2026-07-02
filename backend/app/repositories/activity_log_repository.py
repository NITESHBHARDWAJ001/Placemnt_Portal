from app.models import ActivityLog
from app.repositories.base_repository import BaseRepository


class ActivityLogRepository(BaseRepository):
    model = ActivityLog

    @classmethod
    def query_all(cls):
        return cls.model.query.order_by(cls.model.created_at.desc())

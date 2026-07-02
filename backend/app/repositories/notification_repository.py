from app.models import Notification
from app.repositories.base_repository import BaseRepository


class NotificationRepository(BaseRepository):
    model = Notification

    @classmethod
    def query_by_user(cls, user_id):
        return cls.model.query.filter_by(user_id=user_id).order_by(cls.model.created_at.desc())

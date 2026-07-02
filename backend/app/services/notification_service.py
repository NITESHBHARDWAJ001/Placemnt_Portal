from app.repositories.notification_repository import NotificationRepository
from app.utils.enums import NotificationType
from app.utils.pagination import paginate_query


class NotificationService:
    @staticmethod
    def notify(user_id, title, message, type_=NotificationType.INFO, link=None):
        return NotificationRepository.create(
            user_id=user_id, title=title, message=message, type=type_, link=link
        )

    @staticmethod
    def list_for_user(user_id, page, per_page):
        query = NotificationRepository.query_by_user(user_id)
        return paginate_query(query, page, per_page)

    @staticmethod
    def mark_read(notification_id, user_id):
        from app.utils.exceptions import ForbiddenError, NotFoundError

        notification = NotificationRepository.get_by_id(notification_id)
        if notification is None:
            raise NotFoundError("Notification not found")
        if notification.user_id != user_id:
            raise ForbiddenError("You cannot modify this notification")
        notification.is_read = True
        NotificationRepository.save(notification)
        return notification

    @staticmethod
    def unread_count(user_id):
        return NotificationRepository.query_by_user(user_id).filter_by(is_read=False).count()

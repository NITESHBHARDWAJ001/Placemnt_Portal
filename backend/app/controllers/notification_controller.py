from flask_jwt_extended import get_jwt_identity, jwt_required

from app.schemas.notification_schema import NotificationSchema
from app.services.notification_service import NotificationService
from app.utils.api_response import success_response
from app.utils.pagination import get_pagination_params

notification_schema = NotificationSchema()


class NotificationController:
    @staticmethod
    @jwt_required()
    def list_mine():
        user_id = get_jwt_identity()
        page, per_page = get_pagination_params()
        items, meta = NotificationService.list_for_user(user_id, page, per_page)
        return success_response("Notifications fetched", notification_schema.dump(items, many=True), meta)

    @staticmethod
    @jwt_required()
    def mark_read(notification_id):
        user_id = get_jwt_identity()
        notification = NotificationService.mark_read(notification_id, user_id)
        return success_response("Notification marked as read", notification_schema.dump(notification))

    @staticmethod
    @jwt_required()
    def unread_count():
        user_id = get_jwt_identity()
        count = NotificationService.unread_count(user_id)
        return success_response("Unread count fetched", {"count": count})

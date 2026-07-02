from flask import Blueprint

from app.controllers.notification_controller import NotificationController

notification_bp = Blueprint("notification", __name__, url_prefix="/api/v1/notifications")

notification_bp.add_url_rule("", view_func=NotificationController.list_mine, methods=["GET"])
notification_bp.add_url_rule("/unread-count", view_func=NotificationController.unread_count, methods=["GET"])
notification_bp.add_url_rule("/<int:notification_id>/read", view_func=NotificationController.mark_read, methods=["PATCH"])

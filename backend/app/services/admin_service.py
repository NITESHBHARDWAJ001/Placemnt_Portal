from datetime import datetime, timezone

from app.extensions import db
from app.models import BlacklistLog, User
from app.repositories.user_repository import UserRepository
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService
from app.utils.enums import NotificationType
from app.utils.exceptions import NotFoundError, ValidationError


class AdminService:
    @staticmethod
    def blacklist_user(user_id, admin_user_id, reason):
        user = UserRepository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")
        if user.role.value == "ADMIN":
            raise ValidationError("Admin accounts cannot be blacklisted")

        user.is_blacklisted = True
        log = BlacklistLog(
            user_id=user_id, blacklisted_by=admin_user_id, reason=reason, is_active=True,
            blacklisted_at=datetime.now(timezone.utc),
        )
        db.session.add(log)
        db.session.commit()

        NotificationService.notify(
            user_id, "Account Blacklisted", f"Reason: {reason}", NotificationType.ERROR
        )
        ActivityLogService.log(admin_user_id, "USER_BLACKLISTED", "User", user_id, reason)
        return user

    @staticmethod
    def revoke_blacklist(user_id, admin_user_id):
        user = UserRepository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")
        user.is_blacklisted = False
        BlacklistLog.query.filter_by(user_id=user_id, is_active=True).update(
            {"is_active": False, "revoked_at": datetime.now(timezone.utc)}
        )
        db.session.commit()
        NotificationService.notify(
            user_id, "Blacklist Revoked", "Your account access has been restored.", NotificationType.SUCCESS
        )
        ActivityLogService.log(admin_user_id, "USER_BLACKLIST_REVOKED", "User", user_id)
        return user

    @staticmethod
    def set_active(user_id, admin_user_id, is_active: bool):
        user = UserRepository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")
        if user.role.value == "ADMIN":
            raise ValidationError("Admin accounts cannot be deactivated")
        user.is_active = is_active
        db.session.commit()
        action = "USER_ACTIVATED" if is_active else "USER_DEACTIVATED"
        ActivityLogService.log(admin_user_id, action, "User", user_id)
        return user

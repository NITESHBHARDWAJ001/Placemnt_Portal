from datetime import datetime, timezone

from app.extensions import db
from app.repositories.company_repository import CompanyRepository
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService
from app.utils.enums import CompanyApprovalStatus, NotificationType
from app.utils.exceptions import NotFoundError, ValidationError
from app.utils.pagination import paginate_query


class CompanyService:
    @staticmethod
    def get_profile_by_user_id(user_id):
        profile = CompanyRepository.get_by_user_id(user_id)
        if profile is None:
            raise NotFoundError("Company profile not found")
        return profile

    @staticmethod
    def update_profile(user_id, data: dict):
        profile = CompanyService.get_profile_by_user_id(user_id)
        for key, value in data.items():
            setattr(profile, key, value)
        db.session.commit()
        ActivityLogService.log(user_id, "COMPANY_PROFILE_UPDATED", "CompanyProfile", profile.id)
        return profile

    @staticmethod
    def list_companies(page, per_page, status=None, search=None):
        from app.models import User

        query = CompanyRepository.query_by_status(status)
        if search:
            like = f"%{search}%"
            query = query.join(User, User.id == CompanyRepository.model.user_id).filter(
                db.or_(CompanyRepository.model.company_name.ilike(like), User.email.ilike(like))
            )
        return paginate_query(query, page, per_page)

    @staticmethod
    def approve(company_id, admin_user_id):
        profile = CompanyRepository.get_by_id(company_id)
        if profile is None:
            raise NotFoundError("Company not found")
        profile.approval_status = CompanyApprovalStatus.APPROVED
        profile.approved_by = admin_user_id
        profile.approved_at = datetime.now(timezone.utc)
        db.session.commit()
        NotificationService.notify(
            profile.user_id, "Company Approved",
            "Your company profile has been approved. You can now create placement drives.",
            NotificationType.SUCCESS,
        )
        ActivityLogService.log(admin_user_id, "COMPANY_APPROVED", "CompanyProfile", profile.id)
        return profile

    @staticmethod
    def reject(company_id, admin_user_id, reason=None):
        profile = CompanyRepository.get_by_id(company_id)
        if profile is None:
            raise NotFoundError("Company not found")
        profile.approval_status = CompanyApprovalStatus.REJECTED
        profile.approved_by = admin_user_id
        profile.approved_at = datetime.now(timezone.utc)
        db.session.commit()
        NotificationService.notify(
            profile.user_id, "Company Application Rejected",
            reason or "Your company registration was rejected by the administrator.",
            NotificationType.ERROR,
        )
        ActivityLogService.log(admin_user_id, "COMPANY_REJECTED", "CompanyProfile", profile.id)
        return profile

    @staticmethod
    def ensure_approved(company_profile):
        if company_profile.approval_status != CompanyApprovalStatus.APPROVED:
            raise ValidationError("Your company must be approved by the admin before this action")

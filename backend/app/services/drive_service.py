from datetime import datetime, timezone

from app.extensions import db
from app.repositories.drive_repository import DriveRepository
from app.services.activity_log_service import ActivityLogService
from app.services.company_service import CompanyService
from app.services.dashboard_service import DashboardService
from app.utils.enums import DriveStatus, NotificationType
from app.utils.exceptions import ForbiddenError, NotFoundError
from app.utils.pagination import paginate_query
from app.validators.drive_validators import validate_drive_payload


class DriveService:
    @staticmethod
    def create(company_profile, data: dict):
        CompanyService.ensure_approved(company_profile)
        validate_drive_payload(data)

        allowed_branches = data.pop("allowed_branches", []) or []
        drive = DriveRepository.model(
            company_profile_id=company_profile.id,
            allowed_branches=",".join(allowed_branches),
            status=DriveStatus.PENDING,
            **data,
        )
        db.session.add(drive)
        db.session.commit()
        ActivityLogService.log(
            company_profile.user_id, "DRIVE_CREATED", "PlacementDrive", drive.id, drive.title
        )
        DashboardService.invalidate_admin_caches()
        DashboardService.invalidate_company_cache(company_profile.id)
        return drive

    @staticmethod
    def get_owned_drive(drive_id, company_profile_id):
        drive = DriveRepository.get_by_id(drive_id)
        if drive is None:
            raise NotFoundError("Drive not found")
        if drive.company_profile_id != company_profile_id:
            raise ForbiddenError("You do not own this drive")
        return drive

    @staticmethod
    def update(drive_id, company_profile_id, data: dict):
        drive = DriveService.get_owned_drive(drive_id, company_profile_id)
        validate_drive_payload({**data})

        if "allowed_branches" in data:
            drive.allowed_branches = ",".join(data.pop("allowed_branches") or [])
        for key, value in data.items():
            setattr(drive, key, value)

        # Edits reset the drive back to pending admin review
        drive.status = DriveStatus.PENDING
        drive.approved_by = None
        drive.approved_at = None
        db.session.commit()
        ActivityLogService.log(
            drive.company_profile.user_id, "DRIVE_UPDATED", "PlacementDrive", drive.id, "Drive edited, pending re-approval"
        )
        DashboardService.invalidate_admin_caches()
        DashboardService.invalidate_company_cache(company_profile_id)
        return drive

    @staticmethod
    def delete(drive_id, company_profile_id):
        drive = DriveService.get_owned_drive(drive_id, company_profile_id)
        db.session.delete(drive)
        db.session.commit()
        DashboardService.invalidate_admin_caches()
        DashboardService.invalidate_company_cache(company_profile_id)

    @staticmethod
    def list_for_company(company_profile_id, page, per_page):
        query = DriveRepository.query_by_company(company_profile_id).order_by(
            DriveRepository.model.created_at.desc()
        )
        return paginate_query(query, page, per_page)

    @staticmethod
    def list_approved_for_students(page, per_page, search=None, student_profile=None):
        query = DriveRepository.query_approved().order_by(
            DriveRepository.model.created_at.desc()
        )
        if search:
            like = f"%{search}%"
            query = query.filter(
                db.or_(DriveRepository.model.title.ilike(like), DriveRepository.model.job_role.ilike(like))
            )

        if student_profile is None:
            return paginate_query(query, page, per_page)

        from math import ceil

        from app.validators.eligibility_validators import check_eligibility

        eligible_drives = [d for d in query.all() if check_eligibility(student_profile, d)[0]]
        total = len(eligible_drives)
        start = (page - 1) * per_page
        items = eligible_drives[start : start + per_page]
        meta = {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": ceil(total / per_page) if per_page else 0,
            "has_next": start + per_page < total,
            "has_prev": page > 1,
        }
        return items, meta

    @staticmethod
    def list_pending_for_admin(page, per_page):
        query = DriveRepository.query_by_status(DriveStatus.PENDING.value).order_by(
            DriveRepository.model.created_at.asc()
        )
        return paginate_query(query, page, per_page)

    @staticmethod
    def list_all_for_admin(page, per_page, status=None):
        query = DriveRepository.query_by_status(status).order_by(
            DriveRepository.model.created_at.desc()
        )
        return paginate_query(query, page, per_page)

    @staticmethod
    def approve(drive_id, admin_user_id):
        from app.services.notification_service import NotificationService

        drive = DriveRepository.get_by_id(drive_id)
        if drive is None:
            raise NotFoundError("Drive not found")
        drive.status = DriveStatus.APPROVED
        drive.approved_by = admin_user_id
        drive.approved_at = datetime.now(timezone.utc)
        db.session.commit()
        NotificationService.notify(
            drive.company_profile.user_id, "Drive Approved",
            f"Your drive '{drive.title}' has been approved and is now live.",
            NotificationType.SUCCESS,
        )
        ActivityLogService.log(admin_user_id, "DRIVE_APPROVED", "PlacementDrive", drive.id)
        DashboardService.invalidate_admin_caches()
        DashboardService.invalidate_company_cache(drive.company_profile_id)
        return drive

    @staticmethod
    def reject(drive_id, admin_user_id, reason=None):
        from app.services.notification_service import NotificationService

        drive = DriveRepository.get_by_id(drive_id)
        if drive is None:
            raise NotFoundError("Drive not found")
        drive.status = DriveStatus.REJECTED
        drive.approved_by = admin_user_id
        drive.approved_at = datetime.now(timezone.utc)
        db.session.commit()
        NotificationService.notify(
            drive.company_profile.user_id, "Drive Rejected",
            reason or f"Your drive '{drive.title}' was rejected by the administrator.",
            NotificationType.ERROR,
        )
        ActivityLogService.log(admin_user_id, "DRIVE_REJECTED", "PlacementDrive", drive.id)
        DashboardService.invalidate_admin_caches()
        DashboardService.invalidate_company_cache(drive.company_profile_id)
        return drive

    @staticmethod
    def get_by_id_or_404(drive_id):
        drive = DriveRepository.get_by_id(drive_id)
        if drive is None:
            raise NotFoundError("Drive not found")
        return drive

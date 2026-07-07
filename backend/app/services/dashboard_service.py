from app.extensions import db
from app.models import Application, CompanyProfile, Interview, PlacementDrive, StudentProfile, User
from app.services.cache_service import CacheService
from app.utils.enums import (
    ApplicationStatus,
    CompanyApprovalStatus,
    DriveStatus,
    InterviewStatus,
    PlacementStatus,
    RoleEnum,
)

ADMIN_STATS_CACHE_KEY = "cache:admin:dashboard_stats"
ADMIN_REPORTS_CACHE_KEY = "cache:admin:reports"
COMPANY_STATS_CACHE_KEY = "cache:company:{company_profile_id}:dashboard_stats"
STUDENT_STATS_CACHE_KEY = "cache:student:{student_profile_id}:dashboard_stats"


class DashboardService:
    @staticmethod
    def admin_stats():
        cached = CacheService.get(ADMIN_STATS_CACHE_KEY)
        if cached is not None:
            return cached

        total_students = User.query.filter_by(role=RoleEnum.STUDENT).count()
        total_companies = User.query.filter_by(role=RoleEnum.COMPANY).count()
        pending_companies = CompanyProfile.query.filter_by(
            approval_status=CompanyApprovalStatus.PENDING
        ).count()
        total_drives = PlacementDrive.query.count()
        pending_drives = PlacementDrive.query.filter_by(status=DriveStatus.PENDING).count()
        total_applications = Application.query.count()
        total_selections = Application.query.filter_by(status=ApplicationStatus.SELECTED).count()

        status_breakdown = (
            db.session.query(Application.status, db.func.count(Application.id))
            .group_by(Application.status)
            .all()
        )
        drive_breakdown = (
            db.session.query(PlacementDrive.status, db.func.count(PlacementDrive.id))
            .group_by(PlacementDrive.status)
            .all()
        )

        result = {
            "total_students": total_students,
            "total_companies": total_companies,
            "pending_companies": pending_companies,
            "total_drives": total_drives,
            "pending_drives": pending_drives,
            "total_applications": total_applications,
            "total_selections": total_selections,
            "applications_by_status": {s.value: c for s, c in status_breakdown},
            "drives_by_status": {s.value: c for s, c in drive_breakdown},
        }
        CacheService.set(ADMIN_STATS_CACHE_KEY, result, ttl_seconds=60)
        return result

    @staticmethod
    def company_stats(company_profile_id):
        cache_key = COMPANY_STATS_CACHE_KEY.format(company_profile_id=company_profile_id)
        cached = CacheService.get(cache_key)
        if cached is not None:
            return cached

        drives = PlacementDrive.query.filter_by(company_profile_id=company_profile_id)
        drive_ids = [d.id for d in drives]

        total_drives = len(drive_ids)
        total_applicants = Application.query.filter(Application.drive_id.in_(drive_ids)).count() if drive_ids else 0
        total_selections = (
            Application.query.filter(
                Application.drive_id.in_(drive_ids), Application.status == ApplicationStatus.SELECTED
            ).count()
            if drive_ids
            else 0
        )
        upcoming_interviews = (
            Interview.query.join(Application)
            .filter(Application.drive_id.in_(drive_ids), Interview.status == InterviewStatus.SCHEDULED)
            .count()
            if drive_ids
            else 0
        )

        result = {
            "total_drives": total_drives,
            "total_applicants": total_applicants,
            "total_selections": total_selections,
            "upcoming_interviews": upcoming_interviews,
        }
        CacheService.set(cache_key, result, ttl_seconds=60)
        return result

    @staticmethod
    def admin_reports():
        cached = CacheService.get(ADMIN_REPORTS_CACHE_KEY)
        if cached is not None:
            return cached

        branch_breakdown = (
            db.session.query(StudentProfile.branch, db.func.count(StudentProfile.id))
            .filter(StudentProfile.branch.isnot(None))
            .group_by(StudentProfile.branch)
            .all()
        )

        selections_by_company = (
            db.session.query(CompanyProfile.company_name, db.func.count(Application.id))
            .join(PlacementDrive, PlacementDrive.company_profile_id == CompanyProfile.id)
            .join(Application, Application.drive_id == PlacementDrive.id)
            .filter(Application.status == ApplicationStatus.SELECTED)
            .group_by(CompanyProfile.company_name)
            .order_by(db.func.count(Application.id).desc())
            .limit(10)
            .all()
        )

        monthly_trend = (
            db.session.query(
                db.func.strftime("%Y-%m", Application.applied_at), db.func.count(Application.id)
            )
            .group_by(db.func.strftime("%Y-%m", Application.applied_at))
            .order_by(db.func.strftime("%Y-%m", Application.applied_at))
            .all()
        )

        total_students = User.query.filter_by(role=RoleEnum.STUDENT).count()
        placed_students = StudentProfile.query.filter(
            StudentProfile.placement_status == PlacementStatus.PLACED
        ).count()
        placement_rate = round((placed_students / total_students) * 100, 1) if total_students else 0

        result = {
            "students_by_branch": {b or "Unspecified": c for b, c in branch_breakdown},
            "selections_by_company": {n: c for n, c in selections_by_company},
            "monthly_application_trend": {m: c for m, c in monthly_trend if m},
            "total_students": total_students,
            "placed_students": placed_students,
            "placement_rate_percent": placement_rate,
        }
        CacheService.set(ADMIN_REPORTS_CACHE_KEY, result, ttl_seconds=300)
        return result

    @staticmethod
    def student_stats(student_profile_id):
        cache_key = STUDENT_STATS_CACHE_KEY.format(student_profile_id=student_profile_id)
        cached = CacheService.get(cache_key)
        if cached is not None:
            return cached

        applications = Application.query.filter_by(student_profile_id=student_profile_id)
        total_applied = applications.count()
        selected = applications.filter_by(status=ApplicationStatus.SELECTED).count()
        rejected = applications.filter_by(status=ApplicationStatus.REJECTED).count()
        shortlisted = applications.filter_by(status=ApplicationStatus.SHORTLISTED).count()

        eligible_drives = PlacementDrive.query.filter_by(status=DriveStatus.APPROVED).count()

        result = {
            "eligible_drives": eligible_drives,
            "applied_drives": total_applied,
            "shortlisted": shortlisted,
            "selected_drives": selected,
            "rejected_drives": rejected,
        }
        CacheService.set(cache_key, result, ttl_seconds=60)
        return result

    @staticmethod
    def invalidate_admin_caches():
        CacheService.delete(ADMIN_STATS_CACHE_KEY)
        CacheService.delete(ADMIN_REPORTS_CACHE_KEY)

    @staticmethod
    def invalidate_company_cache(company_profile_id):
        CacheService.delete(COMPANY_STATS_CACHE_KEY.format(company_profile_id=company_profile_id))

    @staticmethod
    def invalidate_student_cache(student_profile_id):
        CacheService.delete(STUDENT_STATS_CACHE_KEY.format(student_profile_id=student_profile_id))

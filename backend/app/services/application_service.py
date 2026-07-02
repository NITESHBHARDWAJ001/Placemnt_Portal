from app.extensions import db
from app.repositories.application_repository import ApplicationRepository
from app.repositories.drive_repository import DriveRepository
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService
from app.services.resume_service import ResumeService
from app.utils.enums import ApplicationStatus, NotificationType, PlacementStatus
from app.utils.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.utils.pagination import paginate_query
from app.validators.application_validators import validate_can_apply


class ApplicationService:
    @staticmethod
    def apply(student_profile, drive_id, resume_id=None):
        drive = DriveRepository.get_by_id(drive_id)
        if drive is None:
            raise NotFoundError("Drive not found")

        existing = ApplicationRepository.get_existing(student_profile.id, drive_id)
        validate_can_apply(student_profile, drive, existing)

        if resume_id:
            resume = ResumeService.get_owned_resume(resume_id, student_profile.id)
        else:
            resume = ResumeService.get_active_resume(student_profile.id)
        if resume is None:
            raise ValidationError("Please upload a resume before applying")

        from app.validators.eligibility_validators import check_eligibility

        is_eligible, reasons = check_eligibility(student_profile, drive)
        if not is_eligible:
            raise ValidationError("You are not eligible for this drive", errors=reasons)

        application = ApplicationRepository.create(
            student_profile_id=student_profile.id,
            drive_id=drive_id,
            resume_id=resume.id,
            status=ApplicationStatus.APPLIED,
        )
        NotificationService.notify(
            drive.company_profile.user_id, "New Applicant",
            f"{student_profile.user.name} applied to '{drive.title}'.",
            NotificationType.INFO,
        )
        ActivityLogService.log(
            student_profile.user_id, "APPLICATION_SUBMITTED", "Application", application.id
        )
        return application

    @staticmethod
    def withdraw(application_id, student_profile_id):
        application = ApplicationRepository.get_by_id(application_id)
        if application is None:
            raise NotFoundError("Application not found")
        if application.student_profile_id != student_profile_id:
            raise ForbiddenError("You cannot withdraw this application")
        if application.status in (ApplicationStatus.SELECTED, ApplicationStatus.REJECTED):
            raise ValidationError("Cannot withdraw an application that is already finalized")
        application.status = ApplicationStatus.WITHDRAWN
        db.session.commit()
        return application

    @staticmethod
    def list_for_student(student_profile_id, page, per_page):
        query = ApplicationRepository.query_by_student(student_profile_id).order_by(
            ApplicationRepository.model.applied_at.desc()
        )
        return paginate_query(query, page, per_page)

    @staticmethod
    def list_all_for_student(student_profile_id):
        """Unpaginated — used for CSV export. Phase 2 will run this inside a
        Celery task instead of the request/response cycle; the query itself
        does not change."""
        return ApplicationRepository.query_by_student(student_profile_id).order_by(
            ApplicationRepository.model.applied_at.desc()
        ).all()

    @staticmethod
    def list_for_drive(drive_id, company_profile_id, page, per_page, search=None, status=None):
        drive = DriveRepository.get_by_id(drive_id)
        if drive is None:
            raise NotFoundError("Drive not found")
        if drive.company_profile_id != company_profile_id:
            raise ForbiddenError("You do not own this drive")

        query = ApplicationRepository.query_by_drive(drive_id)

        if search or status:
            from app.models import StudentProfile, User

            query = query.join(StudentProfile).join(User, User.id == StudentProfile.user_id)
            if search:
                like = f"%{search}%"
                query = query.filter(db.or_(User.name.ilike(like), User.email.ilike(like)))
            if status:
                query = query.filter(ApplicationRepository.model.status == ApplicationStatus(status))

        query = query.order_by(ApplicationRepository.model.applied_at.desc())
        return paginate_query(query, page, per_page)

    @staticmethod
    def list_for_company(company_profile_id, page, per_page):
        query = ApplicationRepository.query_by_company(company_profile_id).order_by(
            ApplicationRepository.model.applied_at.desc()
        )
        return paginate_query(query, page, per_page)

    @staticmethod
    def get_owned_by_company(application_id, company_profile_id):
        application = ApplicationRepository.get_by_id(application_id)
        if application is None:
            raise NotFoundError("Application not found")
        if application.drive.company_profile_id != company_profile_id:
            raise ForbiddenError("You do not have access to this application")
        return application

    @staticmethod
    def update_status(application_id, company_profile_id, new_status: str):
        application = ApplicationService.get_owned_by_company(application_id, company_profile_id)
        application.status = ApplicationStatus(new_status)
        if application.status == ApplicationStatus.SELECTED:
            application.student_profile.placement_status = PlacementStatus.PLACED
        db.session.commit()

        NotificationService.notify(
            application.student_profile.user_id, f"Application {application.status.value.title()}",
            f"Your application to '{application.drive.title}' is now {application.status.value}.",
            NotificationType.SUCCESS if application.status == ApplicationStatus.SELECTED else NotificationType.INFO,
        )
        ActivityLogService.log(
            application.drive.company_profile.user_id,
            "APPLICATION_STATUS_UPDATED",
            "Application",
            application.id,
            application.status.value,
        )
        return application

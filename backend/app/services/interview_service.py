from app.extensions import db
from app.repositories.interview_repository import InterviewRepository
from app.services.application_service import ApplicationService
from app.services.notification_service import NotificationService
from app.utils.enums import ApplicationStatus, NotificationType
from app.utils.exceptions import ForbiddenError, NotFoundError


class InterviewService:
    @staticmethod
    def schedule(application_id, company_profile_id, data: dict):
        application = ApplicationService.get_owned_by_company(application_id, company_profile_id)

        interview = InterviewRepository.create(application_id=application.id, **data)

        application.status = ApplicationStatus.INTERVIEW_SCHEDULED
        db.session.commit()

        NotificationService.notify(
            application.student_profile.user_id, "Interview Scheduled",
            f"An interview round for '{application.drive.title}' has been scheduled.",
            NotificationType.INFO,
        )
        return interview

    @staticmethod
    def update(interview_id, company_profile_id, data: dict):
        interview = InterviewRepository.get_by_id(interview_id)
        if interview is None:
            raise NotFoundError("Interview not found")
        if interview.application.drive.company_profile_id != company_profile_id:
            raise ForbiddenError("You do not have access to this interview")

        for key, value in data.items():
            setattr(interview, key, value)
        db.session.commit()
        return interview

    @staticmethod
    def list_for_company(company_profile_id):
        return InterviewRepository.query_upcoming_by_company(company_profile_id).order_by(
            InterviewRepository.model.scheduled_at.asc()
        ).all()

    @staticmethod
    def list_for_application(application_id):
        return InterviewRepository.query_by_application(application_id).order_by(
            InterviewRepository.model.round_number.asc()
        ).all()

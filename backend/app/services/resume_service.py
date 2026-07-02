from app.extensions import db
from app.models import Resume
from app.utils.exceptions import ForbiddenError, NotFoundError
from app.utils.file_storage import delete_file_if_exists, save_resume_file
from app.validators.file_validators import validate_resume_file


class ResumeService:
    @staticmethod
    def upload(student_profile, file_storage):
        validate_resume_file(file_storage)

        Resume.query.filter_by(student_profile_id=student_profile.id, is_active=True).update(
            {"is_active": False}
        )

        original_name, full_path = save_resume_file(file_storage, student_profile.id)
        resume = Resume(
            student_profile_id=student_profile.id,
            file_name=original_name,
            file_path=full_path,
            is_active=True,
        )
        db.session.add(resume)
        db.session.commit()
        return resume

    @staticmethod
    def get_active_resume(student_profile_id):
        return Resume.query.filter_by(
            student_profile_id=student_profile_id, is_active=True
        ).first()

    @staticmethod
    def list_for_student(student_profile_id):
        return (
            Resume.query.filter_by(student_profile_id=student_profile_id)
            .order_by(Resume.created_at.desc())
            .all()
        )

    @staticmethod
    def get_owned_resume(resume_id, student_profile_id):
        resume = Resume.query.get(resume_id)
        if resume is None:
            raise NotFoundError("Resume not found")
        if resume.student_profile_id != student_profile_id:
            raise ForbiddenError("You cannot access this resume")
        return resume

    @staticmethod
    def delete(resume_id, student_profile_id):
        resume = ResumeService.get_owned_resume(resume_id, student_profile_id)
        delete_file_if_exists(resume.file_path)
        db.session.delete(resume)
        db.session.commit()

from app.extensions import db
from app.repositories.student_repository import StudentRepository
from app.services.activity_log_service import ActivityLogService
from app.utils.exceptions import NotFoundError


class StudentService:
    @staticmethod
    def get_profile_by_user_id(user_id):
        profile = StudentRepository.get_by_user_id(user_id)
        if profile is None:
            raise NotFoundError("Student profile not found")
        return profile

    @staticmethod
    def update_profile(user_id, data: dict):
        profile = StudentService.get_profile_by_user_id(user_id)
        for key, value in data.items():
            setattr(profile, key, value)
        db.session.commit()
        ActivityLogService.log(user_id, "STUDENT_PROFILE_UPDATED", "StudentProfile", profile.id)
        return profile

    @staticmethod
    def add_skill(user_id, skill_name):
        profile = StudentService.get_profile_by_user_id(user_id)
        return StudentRepository.add_skill(profile.id, skill_name.strip())

    @staticmethod
    def remove_skill(user_id, skill_id):
        profile = StudentService.get_profile_by_user_id(user_id)
        StudentRepository.remove_skill(profile.id, skill_id)

    @staticmethod
    def list_students(page, per_page, search=None):
        from app.models import User
        from app.utils.pagination import paginate_query

        query = StudentRepository.query_all()
        if search:
            like = f"%{search}%"
            query = query.filter(db.or_(User.name.ilike(like), User.email.ilike(like)))
        return paginate_query(query, page, per_page)

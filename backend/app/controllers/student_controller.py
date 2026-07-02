from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.middlewares.role_required import role_required
from app.schemas.resume_schema import ResumeSchema
from app.schemas.student_profile_schema import (
    SkillSchema,
    StudentProfileSchema,
    StudentProfileUpdateSchema,
)
from app.services.dashboard_service import DashboardService
from app.services.resume_service import ResumeService
from app.services.student_service import StudentService
from app.utils.api_response import success_response
from app.utils.enums import RoleEnum
from app.utils.exceptions import ValidationError

profile_schema = StudentProfileSchema()
profile_update_schema = StudentProfileUpdateSchema()
skill_schema = SkillSchema()
resume_schema = ResumeSchema()


class StudentController:
    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def get_profile():
        user_id = get_jwt_identity()
        profile = StudentService.get_profile_by_user_id(user_id)
        return success_response("Profile fetched", profile_schema.dump(profile))

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def update_profile():
        user_id = get_jwt_identity()
        data = profile_update_schema.load(request.get_json(force=True), partial=True)
        profile = StudentService.update_profile(user_id, data)
        return success_response("Profile updated", profile_schema.dump(profile))

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def add_skill():
        user_id = get_jwt_identity()
        data = skill_schema.load(request.get_json(force=True))
        StudentService.add_skill(user_id, data["name"])
        profile = StudentService.get_profile_by_user_id(user_id)
        return success_response("Skill added", profile_schema.dump(profile), status_code=201)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def remove_skill(skill_id):
        user_id = get_jwt_identity()
        StudentService.remove_skill(user_id, skill_id)
        profile = StudentService.get_profile_by_user_id(user_id)
        return success_response("Skill removed", profile_schema.dump(profile))

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def upload_resume():
        user_id = get_jwt_identity()
        profile = StudentService.get_profile_by_user_id(user_id)
        file_storage = request.files.get("resume")
        if file_storage is None:
            raise ValidationError("No resume file provided")
        resume = ResumeService.upload(profile, file_storage)
        return success_response("Resume uploaded", resume_schema.dump(resume), status_code=201)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def list_resumes():
        user_id = get_jwt_identity()
        profile = StudentService.get_profile_by_user_id(user_id)
        resumes = ResumeService.list_for_student(profile.id)
        return success_response("Resumes fetched", resume_schema.dump(resumes, many=True))

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def delete_resume(resume_id):
        user_id = get_jwt_identity()
        profile = StudentService.get_profile_by_user_id(user_id)
        ResumeService.delete(resume_id, profile.id)
        return success_response("Resume deleted")

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def dashboard():
        user_id = get_jwt_identity()
        profile = StudentService.get_profile_by_user_id(user_id)
        stats = DashboardService.student_stats(profile.id)
        return success_response("Dashboard stats", stats)

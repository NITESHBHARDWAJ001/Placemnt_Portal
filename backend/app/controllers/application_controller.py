from flask import Response, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.middlewares.role_required import role_required
from app.schemas.application_schema import ApplicationCreateSchema, ApplicationSchema, ApplicationStatusUpdateSchema
from app.services.application_service import ApplicationService
from app.services.company_service import CompanyService
from app.services.student_service import StudentService
from app.utils.api_response import success_response
from app.utils.csv_export import build_applications_csv
from app.utils.enums import RoleEnum
from app.utils.pagination import get_pagination_params

application_schema = ApplicationSchema()
apply_schema = ApplicationCreateSchema()
status_schema = ApplicationStatusUpdateSchema()


class ApplicationController:
    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def apply(drive_id):
        user_id = get_jwt_identity()
        profile = StudentService.get_profile_by_user_id(user_id)
        data = apply_schema.load(request.get_json(silent=True) or {})
        application = ApplicationService.apply(profile, drive_id, data.get("resume_id"))
        return success_response("Application submitted", application_schema.dump(application), status_code=201)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def withdraw(application_id):
        user_id = get_jwt_identity()
        profile = StudentService.get_profile_by_user_id(user_id)
        application = ApplicationService.withdraw(application_id, profile.id)
        return success_response("Application withdrawn", application_schema.dump(application))

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def my_applications():
        user_id = get_jwt_identity()
        profile = StudentService.get_profile_by_user_id(user_id)
        page, per_page = get_pagination_params()
        items, meta = ApplicationService.list_for_student(profile.id, page, per_page)
        return success_response("Applications fetched", application_schema.dump(items, many=True), meta)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def export_my_applications():
        """Synchronous CSV export for Phase 1. Phase 2 will move the CSV
        generation into a Celery task and notify the user when it's ready,
        without touching ApplicationService.list_all_for_student or
        build_applications_csv."""
        user_id = get_jwt_identity()
        profile = StudentService.get_profile_by_user_id(user_id)
        applications = ApplicationService.list_all_for_student(profile.id)
        csv_content = build_applications_csv(applications)
        return Response(
            csv_content,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=my_applications.csv"},
        )

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.COMPANY)
    def list_for_drive(drive_id):
        user_id = get_jwt_identity()
        company_profile = CompanyService.get_profile_by_user_id(user_id)
        page, per_page = get_pagination_params()
        search = request.args.get("search")
        status = request.args.get("status")
        items, meta = ApplicationService.list_for_drive(
            drive_id, company_profile.id, page, per_page, search, status
        )
        return success_response("Applicants fetched", application_schema.dump(items, many=True), meta)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.COMPANY)
    def list_for_company():
        user_id = get_jwt_identity()
        company_profile = CompanyService.get_profile_by_user_id(user_id)
        page, per_page = get_pagination_params()
        items, meta = ApplicationService.list_for_company(company_profile.id, page, per_page)
        return success_response("Applicants fetched", application_schema.dump(items, many=True), meta)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.COMPANY)
    def update_status(application_id):
        user_id = get_jwt_identity()
        company_profile = CompanyService.get_profile_by_user_id(user_id)
        data = status_schema.load(request.get_json(force=True))
        application = ApplicationService.update_status(application_id, company_profile.id, data["status"])
        return success_response("Application status updated", application_schema.dump(application))

from flask import request, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.middlewares.role_required import role_required
from app.models import ExportJob
from app.schemas.application_schema import ApplicationCreateSchema, ApplicationSchema, ApplicationStatusUpdateSchema
from app.services.application_service import ApplicationService
from app.services.company_service import CompanyService
from app.services.student_service import StudentService
from app.utils.api_response import success_response
from app.utils.enums import RoleEnum
from app.utils.exceptions import ForbiddenError, NotFoundError, ValidationError
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
    def trigger_export():
        """Kicks off an async CSV export via Celery and returns immediately.
        The student gets an in-app notification (with a download link) once
        the worker finishes."""
        from app.tasks.export_tasks import export_applications_csv

        user_id = get_jwt_identity()
        profile = StudentService.get_profile_by_user_id(user_id)

        job = ExportJob(user_id=user_id, job_type="APPLICATIONS_CSV", status="PENDING")
        db.session.add(job)
        db.session.commit()

        export_applications_csv.delay(job.id, profile.id, user_id)

        return success_response(
            "Export started — you'll be notified when it's ready",
            {"job_id": job.id, "status": job.status},
            status_code=202,
        )

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def export_status(job_id):
        user_id = get_jwt_identity()
        job = ExportJob.query.get(job_id)
        if job is None:
            raise NotFoundError("Export job not found")
        if str(job.user_id) != str(user_id):
            raise ForbiddenError("You do not have access to this export")
        return success_response(
            "Export status fetched",
            {"job_id": job.id, "status": job.status, "completed_at": job.completed_at},
        )

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def download_export(job_id):
        user_id = get_jwt_identity()
        job = ExportJob.query.get(job_id)
        if job is None:
            raise NotFoundError("Export job not found")
        if str(job.user_id) != str(user_id):
            raise ForbiddenError("You do not have access to this export")
        if job.status != "COMPLETED" or not job.file_path:
            raise ValidationError("Export is not ready yet")
        return send_file(job.file_path, mimetype="text/csv", as_attachment=True, download_name="my_applications.csv")

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

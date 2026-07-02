from flask import request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required, verify_jwt_in_request

from app.middlewares.role_required import role_required
from app.schemas.drive_schema import DriveCreateSchema, DriveSchema, DriveUpdateSchema
from app.services.company_service import CompanyService
from app.services.drive_service import DriveService
from app.services.eligibility_service import EligibilityService
from app.services.student_service import StudentService
from app.utils.api_response import success_response
from app.utils.enums import RoleEnum
from app.utils.pagination import get_pagination_params

drive_schema = DriveSchema()
drive_create_schema = DriveCreateSchema()
drive_update_schema = DriveUpdateSchema()


class DriveController:
    @staticmethod
    def list_public():
        """Approved drives — visible to students (and anyone authenticated).
        Pass eligible_only=true (requires a logged-in student) to filter down
        to drives the current student actually qualifies for."""
        page, per_page = get_pagination_params()
        search = request.args.get("search")
        eligible_only = request.args.get("eligible_only", "false").lower() == "true"

        student_profile = None
        if eligible_only:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            student_profile = StudentService.get_profile_by_user_id(user_id)

        items, meta = DriveService.list_approved_for_students(page, per_page, search, student_profile)
        return success_response("Drives fetched", drive_schema.dump(items, many=True), meta)

    @staticmethod
    def get_detail(drive_id):
        drive = DriveService.get_by_id_or_404(drive_id)
        return success_response("Drive detail", drive_schema.dump(drive))

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def check_eligibility(drive_id):
        user_id = get_jwt_identity()
        profile = StudentService.get_profile_by_user_id(user_id)
        drive = DriveService.get_by_id_or_404(drive_id)
        result = EligibilityService.evaluate(profile, drive)
        return success_response("Eligibility evaluated", result)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.COMPANY)
    def create():
        user_id = get_jwt_identity()
        company_profile = CompanyService.get_profile_by_user_id(user_id)
        data = drive_create_schema.load(request.get_json(force=True))
        drive = DriveService.create(company_profile, data)
        return success_response("Drive created and submitted for approval", drive_schema.dump(drive), status_code=201)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.COMPANY)
    def update(drive_id):
        user_id = get_jwt_identity()
        company_profile = CompanyService.get_profile_by_user_id(user_id)
        data = drive_update_schema.load(request.get_json(force=True), partial=True)
        drive = DriveService.update(drive_id, company_profile.id, data)
        return success_response("Drive updated", drive_schema.dump(drive))

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.COMPANY)
    def delete(drive_id):
        user_id = get_jwt_identity()
        company_profile = CompanyService.get_profile_by_user_id(user_id)
        DriveService.delete(drive_id, company_profile.id)
        return success_response("Drive deleted")

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.COMPANY)
    def list_mine():
        user_id = get_jwt_identity()
        company_profile = CompanyService.get_profile_by_user_id(user_id)
        page, per_page = get_pagination_params()
        items, meta = DriveService.list_for_company(company_profile.id, page, per_page)
        return success_response("Drives fetched", drive_schema.dump(items, many=True), meta)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def list_pending():
        page, per_page = get_pagination_params()
        items, meta = DriveService.list_pending_for_admin(page, per_page)
        return success_response("Pending drives fetched", drive_schema.dump(items, many=True), meta)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def list_all():
        page, per_page = get_pagination_params()
        status = request.args.get("status")
        items, meta = DriveService.list_all_for_admin(page, per_page, status)
        return success_response("Drives fetched", drive_schema.dump(items, many=True), meta)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def approve(drive_id):
        admin_id = get_jwt_identity()
        drive = DriveService.approve(drive_id, admin_id)
        return success_response("Drive approved", drive_schema.dump(drive))

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def reject(drive_id):
        admin_id = get_jwt_identity()
        reason = (request.get_json(silent=True) or {}).get("reason")
        drive = DriveService.reject(drive_id, admin_id, reason)
        return success_response("Drive rejected", drive_schema.dump(drive))

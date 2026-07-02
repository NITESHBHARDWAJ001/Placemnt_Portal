from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.middlewares.role_required import role_required
from app.schemas.activity_log_schema import ActivityLogSchema
from app.schemas.blacklist_schema import BlacklistCreateSchema
from app.schemas.company_profile_schema import CompanyProfileSchema
from app.schemas.student_profile_schema import StudentProfileSchema
from app.services.activity_log_service import ActivityLogService
from app.services.admin_service import AdminService
from app.services.company_service import CompanyService
from app.services.dashboard_service import DashboardService
from app.services.student_service import StudentService
from app.utils.api_response import success_response
from app.utils.enums import RoleEnum
from app.utils.pagination import get_pagination_params

company_schema = CompanyProfileSchema()
student_schema = StudentProfileSchema()
activity_log_schema = ActivityLogSchema()
blacklist_schema = BlacklistCreateSchema()


class AdminController:
    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def dashboard():
        stats = DashboardService.admin_stats()
        return success_response("Dashboard stats", stats)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def reports():
        report = DashboardService.admin_reports()
        return success_response("Reports fetched", report)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def list_companies():
        page, per_page = get_pagination_params()
        status = request.args.get("status")
        search = request.args.get("search")
        items, meta = CompanyService.list_companies(page, per_page, status, search)
        return success_response("Companies fetched", company_schema.dump(items, many=True), meta)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def approve_company(company_id):
        admin_id = get_jwt_identity()
        profile = CompanyService.approve(company_id, admin_id)
        return success_response("Company approved", company_schema.dump(profile))

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def reject_company(company_id):
        admin_id = get_jwt_identity()
        reason = (request.get_json(silent=True) or {}).get("reason")
        profile = CompanyService.reject(company_id, admin_id, reason)
        return success_response("Company rejected", company_schema.dump(profile))

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def list_students():
        page, per_page = get_pagination_params()
        search = request.args.get("search")
        items, meta = StudentService.list_students(page, per_page, search)
        return success_response("Students fetched", student_schema.dump(items, many=True), meta)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def blacklist_user(user_id):
        admin_id = get_jwt_identity()
        data = blacklist_schema.load(request.get_json(force=True))
        AdminService.blacklist_user(user_id, admin_id, data["reason"])
        return success_response("User blacklisted")

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def revoke_blacklist(user_id):
        admin_id = get_jwt_identity()
        AdminService.revoke_blacklist(user_id, admin_id)
        return success_response("Blacklist revoked")

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def deactivate_user(user_id):
        admin_id = get_jwt_identity()
        AdminService.set_active(user_id, admin_id, False)
        return success_response("User deactivated")

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def activate_user(user_id):
        admin_id = get_jwt_identity()
        AdminService.set_active(user_id, admin_id, True)
        return success_response("User activated")

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def activity_logs():
        page, per_page = get_pagination_params()
        items, meta = ActivityLogService.list_logs(page, per_page)
        return success_response("Activity logs fetched", activity_log_schema.dump(items, many=True), meta)

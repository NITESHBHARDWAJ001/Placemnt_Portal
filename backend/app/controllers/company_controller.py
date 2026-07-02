from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.middlewares.role_required import role_required
from app.schemas.company_profile_schema import CompanyProfileSchema, CompanyProfileUpdateSchema
from app.services.company_service import CompanyService
from app.services.dashboard_service import DashboardService
from app.utils.api_response import success_response
from app.utils.enums import RoleEnum

profile_schema = CompanyProfileSchema()
profile_update_schema = CompanyProfileUpdateSchema()


class CompanyController:
    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.COMPANY)
    def get_profile():
        user_id = get_jwt_identity()
        profile = CompanyService.get_profile_by_user_id(user_id)
        return success_response("Profile fetched", profile_schema.dump(profile))

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.COMPANY)
    def update_profile():
        user_id = get_jwt_identity()
        data = profile_update_schema.load(request.get_json(force=True), partial=True)
        profile = CompanyService.update_profile(user_id, data)
        return success_response("Profile updated", profile_schema.dump(profile))

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.COMPANY)
    def dashboard():
        user_id = get_jwt_identity()
        profile = CompanyService.get_profile_by_user_id(user_id)
        stats = DashboardService.company_stats(profile.id)
        return success_response("Dashboard stats", stats)

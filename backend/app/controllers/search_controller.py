from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.middlewares.role_required import role_required
from app.schemas.application_schema import ApplicationSchema
from app.schemas.company_profile_schema import CompanyProfileSchema
from app.schemas.drive_schema import DriveSchema
from app.schemas.student_profile_schema import StudentProfileSchema
from app.services.company_service import CompanyService
from app.services.search_service import SearchService
from app.utils.api_response import success_response
from app.utils.enums import RoleEnum
from app.utils.pagination import get_pagination_params

student_schema = StudentProfileSchema()
company_schema = CompanyProfileSchema()
drive_schema = DriveSchema()
application_schema = ApplicationSchema()


class SearchController:
    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def students():
        term = request.args.get("q", "")
        page, per_page = get_pagination_params()
        items, meta = SearchService.search_students(term, page, per_page)
        return success_response("Results fetched", student_schema.dump(items, many=True), meta)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.ADMIN)
    def companies():
        term = request.args.get("q", "")
        page, per_page = get_pagination_params()
        items, meta = SearchService.search_companies(term, page, per_page)
        return success_response("Results fetched", company_schema.dump(items, many=True), meta)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.STUDENT)
    def drives():
        term = request.args.get("q", "")
        page, per_page = get_pagination_params()
        items, meta = SearchService.search_drives(term, page, per_page)
        return success_response("Results fetched", drive_schema.dump(items, many=True), meta)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.COMPANY)
    def applicants():
        user_id = get_jwt_identity()
        company_profile = CompanyService.get_profile_by_user_id(user_id)
        term = request.args.get("q", "")
        page, per_page = get_pagination_params()
        items, meta = SearchService.search_applicants(company_profile.id, term, page, per_page)
        return success_response("Results fetched", application_schema.dump(items, many=True), meta)

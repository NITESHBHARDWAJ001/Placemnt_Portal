from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.middlewares.role_required import role_required
from app.schemas.interview_schema import InterviewCreateSchema, InterviewSchema, InterviewUpdateSchema
from app.services.company_service import CompanyService
from app.services.interview_service import InterviewService
from app.utils.api_response import success_response
from app.utils.enums import RoleEnum

interview_schema = InterviewSchema()
create_schema = InterviewCreateSchema()
update_schema = InterviewUpdateSchema()


class InterviewController:
    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.COMPANY)
    def schedule(application_id):
        user_id = get_jwt_identity()
        company_profile = CompanyService.get_profile_by_user_id(user_id)
        data = create_schema.load(request.get_json(force=True))
        interview = InterviewService.schedule(application_id, company_profile.id, data)
        return success_response("Interview scheduled", interview_schema.dump(interview), status_code=201)

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.COMPANY)
    def update(interview_id):
        user_id = get_jwt_identity()
        company_profile = CompanyService.get_profile_by_user_id(user_id)
        data = update_schema.load(request.get_json(force=True), partial=True)
        interview = InterviewService.update(interview_id, company_profile.id, data)
        return success_response("Interview updated", interview_schema.dump(interview))

    @staticmethod
    @jwt_required()
    @role_required(RoleEnum.COMPANY)
    def list_for_company():
        user_id = get_jwt_identity()
        company_profile = CompanyService.get_profile_by_user_id(user_id)
        interviews = InterviewService.list_for_company(company_profile.id)
        return success_response("Interviews fetched", interview_schema.dump(interviews, many=True))

    @staticmethod
    @jwt_required()
    def list_for_application(application_id):
        interviews = InterviewService.list_for_application(application_id)
        return success_response("Interviews fetched", interview_schema.dump(interviews, many=True))

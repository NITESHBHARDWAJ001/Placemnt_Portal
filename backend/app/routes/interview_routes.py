from flask import Blueprint

from app.controllers.interview_controller import InterviewController

interview_bp = Blueprint("interview", __name__, url_prefix="/api/v1/interviews")

interview_bp.add_url_rule("/applications/<int:application_id>", view_func=InterviewController.schedule, methods=["POST"])
interview_bp.add_url_rule("/applications/<int:application_id>", view_func=InterviewController.list_for_application, methods=["GET"])
interview_bp.add_url_rule("/company", view_func=InterviewController.list_for_company, methods=["GET"])
interview_bp.add_url_rule("/<int:interview_id>", view_func=InterviewController.update, methods=["PATCH"])

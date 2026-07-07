from flask import Blueprint

from app.controllers.application_controller import ApplicationController

application_bp = Blueprint("application", __name__, url_prefix="/api/v1/applications")

application_bp.add_url_rule("/drives/<int:drive_id>/apply", view_func=ApplicationController.apply, methods=["POST"])
application_bp.add_url_rule("/drives/<int:drive_id>", view_func=ApplicationController.list_for_drive, methods=["GET"])
application_bp.add_url_rule("/mine", view_func=ApplicationController.my_applications, methods=["GET"])
application_bp.add_url_rule("/export", view_func=ApplicationController.trigger_export, methods=["POST"])
application_bp.add_url_rule("/export/<int:job_id>/status", view_func=ApplicationController.export_status, methods=["GET"])
application_bp.add_url_rule("/export/<int:job_id>/download", view_func=ApplicationController.download_export, methods=["GET"])
application_bp.add_url_rule("/company", view_func=ApplicationController.list_for_company, methods=["GET"])
application_bp.add_url_rule("/<int:application_id>/withdraw", view_func=ApplicationController.withdraw, methods=["PATCH"])
application_bp.add_url_rule("/<int:application_id>/status", view_func=ApplicationController.update_status, methods=["PATCH"])

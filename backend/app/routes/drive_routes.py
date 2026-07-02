from flask import Blueprint

from app.controllers.drive_controller import DriveController

drive_bp = Blueprint("drive", __name__, url_prefix="/api/v1/drives")

drive_bp.add_url_rule("/my", view_func=DriveController.list_mine, methods=["GET"])
drive_bp.add_url_rule("/pending", view_func=DriveController.list_pending, methods=["GET"])
drive_bp.add_url_rule("/all", view_func=DriveController.list_all, methods=["GET"])
drive_bp.add_url_rule("", view_func=DriveController.list_public, methods=["GET"])
drive_bp.add_url_rule("", view_func=DriveController.create, methods=["POST"])
drive_bp.add_url_rule("/<int:drive_id>", view_func=DriveController.get_detail, methods=["GET"])
drive_bp.add_url_rule("/<int:drive_id>", view_func=DriveController.update, methods=["PUT"])
drive_bp.add_url_rule("/<int:drive_id>", view_func=DriveController.delete, methods=["DELETE"])
drive_bp.add_url_rule("/<int:drive_id>/eligibility", view_func=DriveController.check_eligibility, methods=["GET"])
drive_bp.add_url_rule("/<int:drive_id>/approve", view_func=DriveController.approve, methods=["PATCH"])
drive_bp.add_url_rule("/<int:drive_id>/reject", view_func=DriveController.reject, methods=["PATCH"])

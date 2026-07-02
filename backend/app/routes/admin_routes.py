from flask import Blueprint

from app.controllers.admin_controller import AdminController

admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1/admin")

admin_bp.add_url_rule("/dashboard", view_func=AdminController.dashboard, methods=["GET"])
admin_bp.add_url_rule("/reports/summary", view_func=AdminController.reports, methods=["GET"])
admin_bp.add_url_rule("/companies", view_func=AdminController.list_companies, methods=["GET"])
admin_bp.add_url_rule("/companies/<int:company_id>/approve", view_func=AdminController.approve_company, methods=["PATCH"])
admin_bp.add_url_rule("/companies/<int:company_id>/reject", view_func=AdminController.reject_company, methods=["PATCH"])
admin_bp.add_url_rule("/students", view_func=AdminController.list_students, methods=["GET"])
admin_bp.add_url_rule("/applications", view_func=AdminController.list_applications, methods=["GET"])
admin_bp.add_url_rule("/users/<int:user_id>/blacklist", view_func=AdminController.blacklist_user, methods=["PATCH"])
admin_bp.add_url_rule("/users/<int:user_id>/revoke-blacklist", view_func=AdminController.revoke_blacklist, methods=["PATCH"])
admin_bp.add_url_rule("/users/<int:user_id>/deactivate", view_func=AdminController.deactivate_user, methods=["PATCH"])
admin_bp.add_url_rule("/users/<int:user_id>/activate", view_func=AdminController.activate_user, methods=["PATCH"])
admin_bp.add_url_rule("/activity-logs", view_func=AdminController.activity_logs, methods=["GET"])

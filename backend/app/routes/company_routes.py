from flask import Blueprint

from app.controllers.company_controller import CompanyController

company_bp = Blueprint("company", __name__, url_prefix="/api/v1/company")

company_bp.add_url_rule("/profile", view_func=CompanyController.get_profile, methods=["GET"])
company_bp.add_url_rule("/profile", view_func=CompanyController.update_profile, methods=["PUT"])
company_bp.add_url_rule("/dashboard", view_func=CompanyController.dashboard, methods=["GET"])

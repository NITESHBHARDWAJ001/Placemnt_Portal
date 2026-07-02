from flask import Blueprint

from app.controllers.search_controller import SearchController

search_bp = Blueprint("search", __name__, url_prefix="/api/v1/search")

search_bp.add_url_rule("/students", view_func=SearchController.students, methods=["GET"])
search_bp.add_url_rule("/companies", view_func=SearchController.companies, methods=["GET"])
search_bp.add_url_rule("/drives", view_func=SearchController.drives, methods=["GET"])
search_bp.add_url_rule("/applicants", view_func=SearchController.applicants, methods=["GET"])

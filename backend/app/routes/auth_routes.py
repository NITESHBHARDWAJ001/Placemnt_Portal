from flask import Blueprint

from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

auth_bp.add_url_rule("/register", view_func=AuthController.register, methods=["POST"])
auth_bp.add_url_rule("/login", view_func=AuthController.login, methods=["POST"])
auth_bp.add_url_rule("/refresh", view_func=AuthController.refresh, methods=["POST"])
auth_bp.add_url_rule("/me", view_func=AuthController.me, methods=["GET"])
auth_bp.add_url_rule("/logout", view_func=AuthController.logout, methods=["POST"])

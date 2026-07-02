from flask import Blueprint

from app.controllers.student_controller import StudentController

student_bp = Blueprint("student", __name__, url_prefix="/api/v1/student")

student_bp.add_url_rule("/profile", view_func=StudentController.get_profile, methods=["GET"])
student_bp.add_url_rule("/profile", view_func=StudentController.update_profile, methods=["PUT"])
student_bp.add_url_rule("/skills", view_func=StudentController.add_skill, methods=["POST"])
student_bp.add_url_rule("/skills/<int:skill_id>", view_func=StudentController.remove_skill, methods=["DELETE"])
student_bp.add_url_rule("/resume", view_func=StudentController.upload_resume, methods=["POST"])
student_bp.add_url_rule("/resume", view_func=StudentController.list_resumes, methods=["GET"])
student_bp.add_url_rule("/resume/<int:resume_id>", view_func=StudentController.delete_resume, methods=["DELETE"])
student_bp.add_url_rule("/dashboard", view_func=StudentController.dashboard, methods=["GET"])

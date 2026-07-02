from app.routes.admin_routes import admin_bp
from app.routes.application_routes import application_bp
from app.routes.auth_routes import auth_bp
from app.routes.company_routes import company_bp
from app.routes.drive_routes import drive_bp
from app.routes.interview_routes import interview_bp
from app.routes.notification_routes import notification_bp
from app.routes.search_routes import search_bp
from app.routes.student_routes import student_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(drive_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(search_bp)

import os

from flask import Flask

from app.config import get_config
from app.extensions import bcrypt, cors, db, jwt, ma, migrate
from app.middlewares.error_handler import register_error_handlers
from app.middlewares.request_logger import register_request_logger
from app.routes import register_blueprints
from app.utils.api_response import error_response
from app.utils.logger import configure_logger


def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object or get_config())

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["EXPORT_FOLDER"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}}, supports_credentials=True)

    from app.celery_app import init_celery

    init_celery(app)

    configure_logger(app)
    register_request_logger(app)
    register_error_handlers(app)
    register_blueprints(app)
    _register_jwt_callbacks(app)

    @app.get("/api/v1/health")
    def health_check():
        from app.utils.api_response import success_response

        return success_response("Service is healthy", {"status": "ok"})

    return app


def _register_jwt_callbacks(app):
    from app.models import TokenBlocklist

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return error_response("Token has expired", None, 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return error_response("Invalid token", None, 401)

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        return error_response("Authentication token is missing", None, 401)

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return error_response("Token has been revoked", None, 401)

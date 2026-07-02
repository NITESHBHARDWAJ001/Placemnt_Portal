from marshmallow import ValidationError as MarshmallowValidationError
from sqlalchemy.exc import IntegrityError

from app.utils.api_response import error_response
from app.utils.exceptions import AppError


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(err):
        return error_response(err.message, err.errors, err.status_code)

    @app.errorhandler(MarshmallowValidationError)
    def handle_marshmallow_error(err):
        return error_response("Validation failed", err.messages, 422)

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(err):
        app.logger.error(f"IntegrityError: {err}")
        return error_response("A database constraint was violated", None, 409)

    @app.errorhandler(404)
    def handle_404(err):
        return error_response("Resource not found", None, 404)

    @app.errorhandler(405)
    def handle_405(err):
        return error_response("Method not allowed", None, 405)

    @app.errorhandler(Exception)
    def handle_generic_error(err):
        app.logger.exception("Unhandled exception")
        return error_response("Internal server error", None, 500)

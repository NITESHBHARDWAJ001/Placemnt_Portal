class AppError(Exception):
    status_code = 400

    def __init__(self, message="Something went wrong", status_code=None, errors=None):
        super().__init__(message)
        self.message = message
        self.errors = errors
        if status_code is not None:
            self.status_code = status_code


class NotFoundError(AppError):
    status_code = 404

    def __init__(self, message="Resource not found", errors=None):
        super().__init__(message, 404, errors)


class ValidationError(AppError):
    status_code = 422

    def __init__(self, message="Validation failed", errors=None):
        super().__init__(message, 422, errors)


class UnauthorizedError(AppError):
    status_code = 401

    def __init__(self, message="Unauthorized", errors=None):
        super().__init__(message, 401, errors)


class ForbiddenError(AppError):
    status_code = 403

    def __init__(self, message="Forbidden", errors=None):
        super().__init__(message, 403, errors)


class ConflictError(AppError):
    status_code = 409

    def __init__(self, message="Conflict", errors=None):
        super().__init__(message, 409, errors)

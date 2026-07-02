from functools import wraps

from flask_jwt_extended import get_jwt, verify_jwt_in_request

from app.utils.exceptions import ForbiddenError, UnauthorizedError


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get("role")
            if role is None:
                raise UnauthorizedError("Authentication required")
            if role not in [r.value if hasattr(r, "value") else r for r in allowed_roles]:
                raise ForbiddenError("You do not have permission to perform this action")
            return fn(*args, **kwargs)

        return wrapper

    return decorator

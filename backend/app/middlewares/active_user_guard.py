from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.models import User
from app.utils.exceptions import ForbiddenError, UnauthorizedError


def active_user_required(fn):
    """Re-checks is_active / is_blacklisted on every request in case status
    changed after the access token was issued."""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user is None:
            raise UnauthorizedError("User no longer exists")
        if not user.is_active:
            raise ForbiddenError("Your account has been deactivated")
        if user.is_blacklisted:
            raise ForbiddenError("Your account has been blacklisted")
        return fn(*args, **kwargs)

    return wrapper

from datetime import datetime, timezone

from app.utils.exceptions import ValidationError


def validate_drive_payload(data: dict):
    deadline = data.get("application_deadline")
    if deadline and isinstance(deadline, datetime):
        deadline_cmp = deadline if deadline.tzinfo else deadline.replace(tzinfo=timezone.utc)
        if deadline_cmp <= datetime.now(timezone.utc):
            raise ValidationError("Application deadline must be in the future")

    package_min = data.get("package_min")
    package_max = data.get("package_max")
    if package_min is not None and package_max is not None and package_min > package_max:
        raise ValidationError("Minimum package cannot be greater than maximum package")

    min_cgpa = data.get("min_cgpa")
    if min_cgpa is not None and (min_cgpa < 0 or min_cgpa > 10):
        raise ValidationError("Minimum CGPA must be between 0 and 10")

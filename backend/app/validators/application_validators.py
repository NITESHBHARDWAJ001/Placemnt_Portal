from datetime import datetime, timezone

from app.utils.enums import CompanyApprovalStatus, DriveStatus
from app.utils.exceptions import ConflictError, ForbiddenError, ValidationError


def validate_can_apply(student_profile, drive, existing_application):
    if existing_application is not None:
        raise ConflictError("You have already applied to this drive")

    if drive.status != DriveStatus.APPROVED:
        raise ForbiddenError("This drive is not open for applications")

    if drive.company_profile.approval_status != CompanyApprovalStatus.APPROVED:
        raise ForbiddenError("This company is not approved yet")

    deadline = drive.application_deadline
    deadline_cmp = deadline if deadline.tzinfo else deadline.replace(tzinfo=timezone.utc)
    if deadline_cmp <= datetime.now(timezone.utc):
        raise ValidationError("Application deadline has passed")

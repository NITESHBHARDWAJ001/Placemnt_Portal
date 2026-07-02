"""CSV building utilities.

Kept as a pure function so it can be reused unchanged when Phase 2 wraps
the export in a Celery task and streams the result via a download link
instead of returning it synchronously.
"""
import csv
import io


def build_applications_csv(applications) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        ["Student ID", "Company Name", "Drive Title", "Application Status", "Applied Date"]
    )
    for application in applications:
        writer.writerow(
            [
                application.student_profile_id,
                application.drive.company_profile.company_name,
                application.drive.title,
                application.status.value,
                application.applied_at.strftime("%Y-%m-%d %H:%M") if application.applied_at else "",
            ]
        )
    return buffer.getvalue()

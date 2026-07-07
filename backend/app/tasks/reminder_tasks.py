import logging
from datetime import datetime, timedelta, timezone

from flask import current_app

from app.celery_app import celery
from app.models import Application, PlacementDrive, StudentProfile
from app.services.email_service import EmailService
from app.services.notification_service import NotificationService
from app.utils.enums import DriveStatus, NotificationType
from app.validators.eligibility_validators import check_eligibility

logger = logging.getLogger(__name__)


@celery.task(name="app.tasks.reminder_tasks.send_daily_deadline_reminders")
def send_daily_deadline_reminders():
    """For every active student, find APPROVED drives they're eligible for,
    haven't applied to yet, and whose deadline falls within the reminder
    window — then notify them in-app and by email."""
    window_days = current_app.config["ADMIN_REMINDER_WINDOW_DAYS"]
    now = datetime.now(timezone.utc)
    window_end = now + timedelta(days=window_days)

    upcoming_drives = PlacementDrive.query.filter(
        PlacementDrive.status == DriveStatus.APPROVED,
        PlacementDrive.application_deadline >= now,
        PlacementDrive.application_deadline <= window_end,
    ).all()

    if not upcoming_drives:
        return {"students_notified": 0, "drives_considered": 0}

    already_applied = {
        (a.student_profile_id, a.drive_id)
        for a in Application.query.with_entities(Application.student_profile_id, Application.drive_id)
    }

    students = StudentProfile.query.filter(StudentProfile.cgpa.isnot(None)).all()

    notified = 0
    for student in students:
        if not student.user or not student.user.is_active or student.user.is_blacklisted:
            continue

        matching = [
            drive
            for drive in upcoming_drives
            if (student.id, drive.id) not in already_applied and check_eligibility(student, drive)[0]
        ]
        if not matching:
            continue

        items_html = "".join(
            f"<li><strong>{d.title}</strong> — closes {d.application_deadline.strftime('%d %b %Y, %I:%M %p')}</li>"
            for d in matching
        )
        EmailService.send(
            to_email=student.user.email,
            subject="Placement Drive Deadlines Closing Soon",
            html_body=(
                f"<p>Hi {student.user.name},</p>"
                f"<p>You're eligible for these placement drives closing within "
                f"the next {window_days} day(s):</p><ul>{items_html}</ul>"
                f"<p>Log in to the Placement Portal to apply before the deadline.</p>"
            ),
        )
        NotificationService.notify(
            student.user_id,
            "Deadline Reminder",
            f"{len(matching)} eligible drive(s) closing within {window_days} day(s). Apply now!",
            NotificationType.WARNING,
            link="/student/drives",
        )
        notified += 1

    logger.info(f"[send_daily_deadline_reminders] notified={notified} drives_considered={len(upcoming_drives)}")
    return {"students_notified": notified, "drives_considered": len(upcoming_drives)}

import calendar
import logging
from datetime import datetime, timedelta, timezone

from app.celery_app import celery
from app.models import Application, PlacementDrive, User
from app.services.email_service import EmailService
from app.utils.enums import ApplicationStatus, RoleEnum

logger = logging.getLogger(__name__)


@celery.task(name="app.tasks.report_tasks.send_monthly_activity_report")
def send_monthly_activity_report():
    """Runs on the 1st of every month (Celery Beat). Summarizes the previous
    calendar month's placement activity and emails it to the admin."""
    now = datetime.now(timezone.utc)
    first_of_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    period_end = first_of_this_month - timedelta(seconds=1)
    period_start = period_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    drives_conducted = PlacementDrive.query.filter(
        PlacementDrive.created_at >= period_start, PlacementDrive.created_at <= period_end
    ).count()

    period_applications = Application.query.filter(
        Application.applied_at >= period_start, Application.applied_at <= period_end
    )
    students_applied = period_applications.count()
    students_selected = period_applications.filter(Application.status == ApplicationStatus.SELECTED).count()

    admin = User.query.filter_by(role=RoleEnum.ADMIN).first()
    if admin is None:
        logger.warning("[send_monthly_activity_report] no admin user found, skipping")
        return {"sent": False, "reason": "no admin user"}

    month_label = f"{calendar.month_name[period_start.month]} {period_start.year}"
    html = f"""
    <h2>Monthly Placement Activity Report</h2>
    <p>Period: <strong>{month_label}</strong></p>
    <table cellpadding="8" cellspacing="0" border="1" style="border-collapse:collapse">
      <tr><td>Placement drives conducted</td><td><strong>{drives_conducted}</strong></td></tr>
      <tr><td>Students applied</td><td><strong>{students_applied}</strong></td></tr>
      <tr><td>Students selected</td><td><strong>{students_selected}</strong></td></tr>
    </table>
    <p>— Placement Portal automated report</p>
    """

    sent = EmailService.send(admin.email, f"Monthly Placement Report — {month_label}", html)
    logger.info(f"[send_monthly_activity_report] sent={sent} month={month_label}")
    return {
        "sent": sent,
        "month": month_label,
        "drives_conducted": drives_conducted,
        "students_applied": students_applied,
        "students_selected": students_selected,
    }

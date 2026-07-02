"""Phase-2 placeholder.

In Phase 2, calls here will be dispatched as Celery tasks (daily reminder
emails, monthly report emails). In Phase 1 we just log the intent so the
call sites don't need to change later.
"""

import logging

logger = logging.getLogger(__name__)


class EmailService:
    @staticmethod
    def send_async(to_email: str, subject: str, template: str, context: dict = None):
        logger.info(f"[EmailService placeholder] Would send '{subject}' to {to_email}")
        return True

    @staticmethod
    def queue_daily_reminders():
        logger.info("[EmailService placeholder] Daily reminders will run via Celery Beat in Phase 2")

    @staticmethod
    def queue_monthly_report():
        logger.info("[EmailService placeholder] Monthly report will run via Celery Beat in Phase 2")

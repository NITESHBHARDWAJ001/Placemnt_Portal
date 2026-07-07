"""SMTP email sending.

Uses stdlib smtplib so it works identically inside a normal Flask request
and inside a Celery task (both run with an app context, so current_app.config
is always available). If MAIL_* isn't configured, sends are logged instead of
attempted — lets the rest of the app (and the demo) work before SMTP is set up.
"""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app

logger = logging.getLogger(__name__)


class EmailService:
    @staticmethod
    def send(to_email: str, subject: str, html_body: str) -> bool:
        host = current_app.config.get("MAIL_SERVER")
        port = current_app.config.get("MAIL_PORT")
        username = current_app.config.get("MAIL_USERNAME")
        password = current_app.config.get("MAIL_PASSWORD")
        sender = current_app.config.get("MAIL_DEFAULT_SENDER") or username

        if not host or not username or not password:
            logger.info(f"[EmailService] SMTP not configured — would send '{subject}' to {to_email}")
            return False

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = to_email
        message.attach(MIMEText(html_body, "html"))

        try:
            with smtplib.SMTP(host, port, timeout=10) as server:
                if current_app.config.get("MAIL_USE_TLS", True):
                    server.starttls()
                server.login(username, password)
                server.sendmail(sender, [to_email], message.as_string())
            logger.info(f"[EmailService] Sent '{subject}' to {to_email}")
            return True
        except Exception as e:
            logger.error(f"[EmailService] Failed to send '{subject}' to {to_email}: {e}")
            return False

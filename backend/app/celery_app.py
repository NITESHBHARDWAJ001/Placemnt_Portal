"""Celery instance shared by the Flask app and the worker/beat entrypoint.

Tasks import `celery` from this module (`from app.celery_app import celery`)
so they register on the same instance the CLI (`celery -A celery_worker.celery`)
picks up. `init_celery(app)` binds every task run to a Flask app context so
tasks can use the ORM, current_app.config, etc. exactly like a request does.
"""

from celery import Celery
from celery.schedules import crontab

celery = Celery(__name__)


def init_celery(app):
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["CELERY_RESULT_BACKEND"]
    celery.conf.timezone = "Asia/Kolkata"
    celery.conf.enable_utc = True

    celery.conf.beat_schedule = {
        "daily-deadline-reminders": {
            "task": "app.tasks.reminder_tasks.send_daily_deadline_reminders",
            "schedule": crontab(hour=9, minute=0),
        },
        "monthly-activity-report": {
            "task": "app.tasks.report_tasks.send_monthly_activity_report",
            "schedule": crontab(day_of_month=1, hour=8, minute=0),
        },
    }

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

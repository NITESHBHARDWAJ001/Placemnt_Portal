import logging
import os
from datetime import datetime, timezone

from flask import current_app

from app.celery_app import celery
from app.extensions import db
from app.models import ExportJob
from app.services.application_service import ApplicationService
from app.services.notification_service import NotificationService
from app.utils.csv_export import build_applications_csv
from app.utils.enums import NotificationType

logger = logging.getLogger(__name__)


@celery.task(name="app.tasks.export_tasks.export_applications_csv")
def export_applications_csv(export_job_id: int, student_profile_id: int, user_id: int):
    job = ExportJob.query.get(export_job_id)
    if job is None:
        logger.error(f"[export_applications_csv] job {export_job_id} not found")
        return

    try:
        job.status = "PROCESSING"
        db.session.commit()

        applications = ApplicationService.list_all_for_student(student_profile_id)
        csv_content = build_applications_csv(applications)

        export_dir = current_app.config["EXPORT_FOLDER"]
        os.makedirs(export_dir, exist_ok=True)
        file_name = f"applications_{student_profile_id}_{export_job_id}.csv"
        file_path = os.path.join(export_dir, file_name)
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            f.write(csv_content)

        job.status = "COMPLETED"
        job.file_path = file_path
        job.completed_at = datetime.now(timezone.utc)
        db.session.commit()

        NotificationService.notify(
            user_id,
            "Export Ready",
            "Your applications CSV export is ready to download.",
            NotificationType.SUCCESS,
            link=f"/applications/export/{export_job_id}/download",
        )
        return {"status": "COMPLETED", "file_path": file_path}
    except Exception as e:
        logger.exception(f"[export_applications_csv] failed for job {export_job_id}")
        job.status = "FAILED"
        db.session.commit()
        NotificationService.notify(
            user_id,
            "Export Failed",
            "Something went wrong generating your applications export.",
            NotificationType.ERROR,
        )
        return {"status": "FAILED", "error": str(e)}

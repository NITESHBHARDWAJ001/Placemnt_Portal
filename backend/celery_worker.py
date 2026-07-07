"""Entrypoint for the Celery worker/beat processes.

Run from backend/ with the venv active:
  celery -A celery_worker.celery worker --loglevel=info --pool=solo -B

--pool=solo is required on Windows (no fork()). -B runs an embedded beat
scheduler in the same process, which is fine for local dev/demo; in a real
deployment you'd run `worker` and `beat` as separate processes/services.
"""
from dotenv import load_dotenv

load_dotenv()

from app import create_app  # noqa: E402
from app.celery_app import init_celery  # noqa: E402

flask_app = create_app()
celery = init_celery(flask_app)

# Import task modules so their @celery.task definitions register.
from app.tasks import export_tasks, reminder_tasks, report_tasks  # noqa: E402,F401

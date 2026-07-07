from app.extensions import db
from app.models.base import BaseModel


class ExportJob(BaseModel):
    __tablename__ = "export_jobs"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    job_type = db.Column(db.String(50), nullable=False, default="APPLICATIONS_CSV")
    status = db.Column(db.String(20), nullable=False, default="PENDING")
    file_path = db.Column(db.String(500), nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

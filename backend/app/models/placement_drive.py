from app.extensions import db
from app.models.base import BaseModel
from app.utils.enums import DriveStatus, JobType


class PlacementDrive(BaseModel):
    __tablename__ = "placement_drives"

    company_profile_id = db.Column(
        db.Integer, db.ForeignKey("company_profiles.id"), nullable=False
    )

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    job_role = db.Column(db.String(150))
    job_type = db.Column(db.Enum(JobType), default=JobType.FULL_TIME, nullable=False)
    package_min = db.Column(db.Float)
    package_max = db.Column(db.Float)
    location = db.Column(db.String(150))

    min_cgpa = db.Column(db.Float, default=0)
    max_backlogs = db.Column(db.Integer, default=0)
    allowed_branches = db.Column(db.String(500))  # comma-separated
    eligible_batch = db.Column(db.Integer, nullable=True)

    application_deadline = db.Column(db.DateTime, nullable=False)
    drive_date = db.Column(db.DateTime, nullable=True)

    status = db.Column(db.Enum(DriveStatus), default=DriveStatus.PENDING, nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)

    company_profile = db.relationship("CompanyProfile", back_populates="drives")
    applications = db.relationship(
        "Application", back_populates="drive", cascade="all, delete-orphan"
    )

    def branches_list(self):
        if not self.allowed_branches:
            return []
        return [b.strip() for b in self.allowed_branches.split(",") if b.strip()]

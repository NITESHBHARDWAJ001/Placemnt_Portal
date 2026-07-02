from app.extensions import db
from app.models.base import BaseModel
from app.utils.enums import ApplicationStatus


class Application(BaseModel):
    __tablename__ = "applications"

    student_profile_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id"), nullable=False
    )
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id"), nullable=True)

    status = db.Column(
        db.Enum(ApplicationStatus), default=ApplicationStatus.APPLIED, nullable=False
    )
    applied_at = db.Column(db.DateTime, default=db.func.now())

    student_profile = db.relationship("StudentProfile", back_populates="applications")
    drive = db.relationship("PlacementDrive", back_populates="applications")
    resume = db.relationship("Resume")
    interviews = db.relationship(
        "Interview", back_populates="application", cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.UniqueConstraint("student_profile_id", "drive_id", name="uq_student_drive_application"),
    )

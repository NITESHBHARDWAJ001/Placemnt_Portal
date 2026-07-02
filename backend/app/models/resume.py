from app.extensions import db
from app.models.base import BaseModel


class Resume(BaseModel):
    __tablename__ = "resumes"

    student_profile_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id"), nullable=False
    )
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    student_profile = db.relationship("StudentProfile", back_populates="resumes")

from app.extensions import db
from app.models.base import BaseModel
from app.utils.enums import CompanyApprovalStatus


class CompanyProfile(BaseModel):
    __tablename__ = "company_profiles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    company_name = db.Column(db.String(150), nullable=False)
    website = db.Column(db.String(255))
    industry = db.Column(db.String(120))
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(255))
    hr_name = db.Column(db.String(120))
    hr_designation = db.Column(db.String(120))

    approval_status = db.Column(
        db.Enum(CompanyApprovalStatus), default=CompanyApprovalStatus.PENDING, nullable=False
    )
    approved_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="company_profile", foreign_keys=[user_id])
    drives = db.relationship(
        "PlacementDrive", back_populates="company_profile", cascade="all, delete-orphan"
    )

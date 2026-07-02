from app.extensions import db
from app.models.base import BaseModel
from app.utils.enums import InterviewMode, InterviewResult, InterviewStatus


class Interview(BaseModel):
    __tablename__ = "interviews"

    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False)

    round_number = db.Column(db.Integer, default=1, nullable=False)
    round_name = db.Column(db.String(120))
    scheduled_at = db.Column(db.DateTime, nullable=False)
    mode = db.Column(db.Enum(InterviewMode), default=InterviewMode.ONLINE, nullable=False)
    location_or_link = db.Column(db.String(255))
    interviewer_name = db.Column(db.String(120))

    status = db.Column(db.Enum(InterviewStatus), default=InterviewStatus.SCHEDULED, nullable=False)
    result = db.Column(db.Enum(InterviewResult), default=InterviewResult.PENDING, nullable=False)
    feedback = db.Column(db.Text)

    application = db.relationship("Application", back_populates="interviews")

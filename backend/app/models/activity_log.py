from app.extensions import db
from app.models.base import BaseModel


class ActivityLog(BaseModel):
    __tablename__ = "activity_logs"

    actor_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    entity_type = db.Column(db.String(80), nullable=True)
    entity_id = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(500), nullable=True)
    ip_address = db.Column(db.String(64), nullable=True)

    actor = db.relationship("User", foreign_keys=[actor_user_id])

from app.extensions import db
from app.models.base import BaseModel


class BlacklistLog(BaseModel):
    __tablename__ = "blacklist_logs"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    blacklisted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reason = db.Column(db.String(500), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    blacklisted_at = db.Column(db.DateTime, default=db.func.now())
    revoked_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", foreign_keys=[user_id])
    admin = db.relationship("User", foreign_keys=[blacklisted_by])

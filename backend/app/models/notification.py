from app.extensions import db
from app.models.base import BaseModel
from app.utils.enums import NotificationType


class Notification(BaseModel):
    __tablename__ = "notifications"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    type = db.Column(db.Enum(NotificationType), default=NotificationType.INFO, nullable=False)
    link = db.Column(db.String(255), nullable=True)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship("User", back_populates="notifications")

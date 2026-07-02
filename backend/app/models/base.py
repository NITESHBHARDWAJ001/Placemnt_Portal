from datetime import datetime, timezone

from app.extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class BaseModel(db.Model, TimestampMixin):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

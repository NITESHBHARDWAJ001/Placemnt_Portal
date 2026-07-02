from app.extensions import db
from app.models.base import BaseModel


class TokenBlocklist(BaseModel):
    __tablename__ = "token_blocklist"

    jti = db.Column(db.String(64), nullable=False, unique=True, index=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

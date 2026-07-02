from app.extensions import db
from app.models.base import BaseModel


class Skill(BaseModel):
    __tablename__ = "skills"

    name = db.Column(db.String(80), unique=True, nullable=False)


class StudentSkill(BaseModel):
    __tablename__ = "student_skills"

    student_profile_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id"), nullable=False
    )
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id"), nullable=False)

    skill = db.relationship("Skill")

    __table_args__ = (
        db.UniqueConstraint("student_profile_id", "skill_id", name="uq_student_skill"),
    )

from app.extensions import db
from app.models.base import BaseModel
from app.utils.enums import PlacementStatus


class StudentProfile(BaseModel):
    __tablename__ = "student_profiles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    phone = db.Column(db.String(20))
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(20))
    address = db.Column(db.String(255))
    degree = db.Column(db.String(120))
    branch = db.Column(db.String(120))
    batch_year = db.Column(db.Integer)
    cgpa = db.Column(db.Float)
    backlog_count = db.Column(db.Integer, default=0)
    linkedin_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    portfolio_url = db.Column(db.String(255))
    placement_status = db.Column(
        db.Enum(PlacementStatus), default=PlacementStatus.NOT_PLACED, nullable=False
    )

    user = db.relationship("User", back_populates="student_profile")
    skills = db.relationship(
        "StudentSkill", backref="student_profile", cascade="all, delete-orphan"
    )
    resumes = db.relationship(
        "Resume", back_populates="student_profile", cascade="all, delete-orphan"
    )
    applications = db.relationship(
        "Application", back_populates="student_profile", cascade="all, delete-orphan"
    )

    @property
    def profile_completion_percent(self):
        fields = [
            self.phone, self.dob, self.gender, self.address, self.degree,
            self.branch, self.batch_year, self.cgpa, self.linkedin_url,
        ]
        filled = sum(1 for f in fields if f not in (None, ""))
        return round((filled / len(fields)) * 100)

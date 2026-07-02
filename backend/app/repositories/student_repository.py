from app.models import Skill, StudentProfile, StudentSkill
from app.repositories.base_repository import BaseRepository


class StudentRepository(BaseRepository):
    model = StudentProfile

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.model.query.filter_by(user_id=user_id).first()

    @classmethod
    def query_all(cls):
        return cls.model.query.join(cls.model.user)

    @classmethod
    def add_skill(cls, student_profile_id, skill_name):
        skill = Skill.query.filter(Skill.name.ilike(skill_name)).first()
        if skill is None:
            skill = Skill(name=skill_name)
            from app.extensions import db

            db.session.add(skill)
            db.session.flush()

        existing = StudentSkill.query.filter_by(
            student_profile_id=student_profile_id, skill_id=skill.id
        ).first()
        if existing:
            return existing

        from app.extensions import db

        student_skill = StudentSkill(student_profile_id=student_profile_id, skill_id=skill.id)
        db.session.add(student_skill)
        db.session.commit()
        return student_skill

    @classmethod
    def remove_skill(cls, student_profile_id, skill_id):
        from app.extensions import db

        StudentSkill.query.filter_by(
            student_profile_id=student_profile_id, skill_id=skill_id
        ).delete()
        db.session.commit()

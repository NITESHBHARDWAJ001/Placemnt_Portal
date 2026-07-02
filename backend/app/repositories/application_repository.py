from app.models import Application
from app.repositories.base_repository import BaseRepository


class ApplicationRepository(BaseRepository):
    model = Application

    @classmethod
    def get_existing(cls, student_profile_id, drive_id):
        return cls.model.query.filter_by(
            student_profile_id=student_profile_id, drive_id=drive_id
        ).first()

    @classmethod
    def query_by_student(cls, student_profile_id):
        return cls.model.query.filter_by(student_profile_id=student_profile_id)

    @classmethod
    def query_by_drive(cls, drive_id):
        return cls.model.query.filter_by(drive_id=drive_id)

    @classmethod
    def query_by_company(cls, company_profile_id):
        from app.models import PlacementDrive

        return cls.model.query.join(PlacementDrive).filter(
            PlacementDrive.company_profile_id == company_profile_id
        )

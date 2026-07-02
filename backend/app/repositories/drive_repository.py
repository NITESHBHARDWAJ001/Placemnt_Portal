from app.models import PlacementDrive
from app.repositories.base_repository import BaseRepository
from app.utils.enums import DriveStatus


class DriveRepository(BaseRepository):
    model = PlacementDrive

    @classmethod
    def query_by_status(cls, status: str = None):
        query = cls.model.query
        if status:
            query = query.filter(cls.model.status == DriveStatus(status))
        return query

    @classmethod
    def query_by_company(cls, company_profile_id):
        return cls.model.query.filter_by(company_profile_id=company_profile_id)

    @classmethod
    def query_approved(cls):
        return cls.model.query.filter(cls.model.status == DriveStatus.APPROVED)

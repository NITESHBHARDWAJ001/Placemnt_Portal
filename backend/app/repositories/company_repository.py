from app.models import CompanyProfile
from app.repositories.base_repository import BaseRepository
from app.utils.enums import CompanyApprovalStatus


class CompanyRepository(BaseRepository):
    model = CompanyProfile

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.model.query.filter_by(user_id=user_id).first()

    @classmethod
    def query_by_status(cls, status: str = None):
        query = cls.model.query
        if status:
            query = query.filter(cls.model.approval_status == CompanyApprovalStatus(status))
        return query

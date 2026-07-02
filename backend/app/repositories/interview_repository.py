from app.models import Interview
from app.repositories.base_repository import BaseRepository


class InterviewRepository(BaseRepository):
    model = Interview

    @classmethod
    def query_by_application(cls, application_id):
        return cls.model.query.filter_by(application_id=application_id)

    @classmethod
    def query_upcoming_by_company(cls, company_profile_id):
        from app.models import Application, PlacementDrive

        return (
            cls.model.query.join(Application)
            .join(PlacementDrive)
            .filter(PlacementDrive.company_profile_id == company_profile_id)
        )

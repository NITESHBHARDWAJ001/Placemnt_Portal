from app.extensions import db
from app.models import Application, CompanyProfile, PlacementDrive, StudentProfile, User
from app.utils.pagination import paginate_query


class SearchService:
    @staticmethod
    def search_students(term, page, per_page):
        like = f"%{term}%"
        query = StudentProfile.query.join(User).filter(
            db.or_(User.name.ilike(like), User.email.ilike(like), StudentProfile.branch.ilike(like))
        )
        return paginate_query(query, page, per_page)

    @staticmethod
    def search_companies(term, page, per_page, status=None):
        from app.utils.enums import CompanyApprovalStatus

        like = f"%{term}%"
        query = CompanyProfile.query.join(User, User.id == CompanyProfile.user_id).filter(
            db.or_(CompanyProfile.company_name.ilike(like), User.email.ilike(like))
        )
        if status:
            query = query.filter(CompanyProfile.approval_status == CompanyApprovalStatus(status))
        return paginate_query(query, page, per_page)

    @staticmethod
    def search_drives(term, page, per_page):
        like = f"%{term}%"
        query = PlacementDrive.query.filter(
            db.or_(PlacementDrive.title.ilike(like), PlacementDrive.job_role.ilike(like))
        )
        return paginate_query(query, page, per_page)

    @staticmethod
    def search_applicants(company_profile_id, term, page, per_page):
        like = f"%{term}%"
        query = (
            Application.query.join(PlacementDrive)
            .join(StudentProfile)
            .join(User, User.id == StudentProfile.user_id)
            .filter(PlacementDrive.company_profile_id == company_profile_id)
            .filter(db.or_(User.name.ilike(like), User.email.ilike(like)))
        )
        return paginate_query(query, page, per_page)

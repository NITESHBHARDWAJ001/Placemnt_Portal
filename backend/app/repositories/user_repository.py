from app.models import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    model = User

    @classmethod
    def get_by_email(cls, email):
        return cls.model.query.filter(cls.model.email.ilike(email)).first()

    @classmethod
    def email_exists(cls, email):
        return cls.get_by_email(email) is not None

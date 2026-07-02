from app.extensions import db


class BaseRepository:
    model = None

    @classmethod
    def get_by_id(cls, entity_id):
        return cls.model.query.get(entity_id)

    @classmethod
    def get_all(cls):
        return cls.model.query.all()

    @classmethod
    def create(cls, **kwargs):
        instance = cls.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def save(cls, instance):
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def delete(cls, instance):
        db.session.delete(instance)
        db.session.commit()

    @staticmethod
    def commit():
        db.session.commit()

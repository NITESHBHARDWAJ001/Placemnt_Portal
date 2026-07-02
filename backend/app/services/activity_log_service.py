from flask import request

from app.repositories.activity_log_repository import ActivityLogRepository


class ActivityLogService:
    @staticmethod
    def log(actor_user_id, action, entity_type=None, entity_id=None, description=None):
        try:
            ip = request.remote_addr if request else None
        except RuntimeError:
            ip = None
        ActivityLogRepository.create(
            actor_user_id=actor_user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            ip_address=ip,
        )

    @staticmethod
    def list_logs(page, per_page):
        from app.utils.pagination import paginate_query

        query = ActivityLogRepository.query_all()
        return paginate_query(query, page, per_page)

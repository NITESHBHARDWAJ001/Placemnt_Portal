from flask import request, current_app


def get_pagination_params():
    try:
        page = int(request.args.get("page", current_app.config["PAGINATION_DEFAULT_PAGE"]))
    except (TypeError, ValueError):
        page = current_app.config["PAGINATION_DEFAULT_PAGE"]

    try:
        per_page = int(
            request.args.get("per_page", current_app.config["PAGINATION_DEFAULT_PER_PAGE"])
        )
    except (TypeError, ValueError):
        per_page = current_app.config["PAGINATION_DEFAULT_PER_PAGE"]

    page = max(page, 1)
    per_page = min(max(per_page, 1), current_app.config["PAGINATION_MAX_PER_PAGE"])
    return page, per_page


def paginate_query(query, page, per_page):
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    meta = {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "total_pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
    }
    return pagination.items, meta

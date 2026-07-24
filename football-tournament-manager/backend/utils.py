from functools import wraps
from flask import request
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from extensions import db


def paginate_query(query, schema, default_page=1, default_per_page=10, max_per_page=100):
    """Shared pagination helper returning {page, per_page, total, total_pages, data}."""
    try:
        page = int(request.args.get("page", default_page))
    except (TypeError, ValueError):
        page = default_page
    try:
        per_page = int(request.args.get("per_page", default_per_page))
    except (TypeError, ValueError):
        per_page = default_per_page

    page = max(page, 1)
    per_page = max(1, min(per_page, max_per_page))

    pagination = db.paginate(query, page=page, per_page=per_page, error_out=False)

    return {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "total_pages": pagination.pages,
        "data": schema.dump(pagination.items),
    }


def roles_required(*roles):
    """Decorator enforcing that the current JWT user's role is one of `roles`."""

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get("role")
            if role not in roles:
                return {"message": "Forbidden: insufficient permissions"}, 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
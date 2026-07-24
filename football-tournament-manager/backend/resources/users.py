from flask import request
from flask_restful import Resource

from extensions import db
from models import User
from schemas import user_schema, users_schema
from utils import paginate_query, roles_required
from config import Config


class UserListResource(Resource):
    @roles_required("admin")
    def get(self):
        query = db.select(User).order_by(User.id)
        return paginate_query(
            query, users_schema,
            Config.DEFAULT_PAGE, Config.DEFAULT_PER_PAGE, Config.MAX_PER_PAGE,
        ), 200


class UserResource(Resource):
    @roles_required("admin", "manager", "player")
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user), 200

    @roles_required("admin")
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        payload = request.get_json() or {}
        if "role" in payload:
            user.role = payload["role"]
        if "email" in payload:
            user.email = payload["email"]
        db.session.commit()
        return user_schema.dump(user), 200

    @roles_required("admin")
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from marshmallow import ValidationError

from extensions import db
from models import User, Profile
from schemas import user_schema


class RegisterResource(Resource):
    def post(self):
        payload = request.get_json() or {}
        try:
            data = user_schema.load(payload, partial=("role",))
        except ValidationError as err:
            return {"errors": err.messages}, 400

        password = payload.get("password")
        if not password or len(password) < 6:
            return {"errors": {"password": ["Password must be at least 6 characters."]}}, 400

        if User.query.filter_by(username=data["username"]).first():
            return {"message": "Username already taken"}, 409
        if User.query.filter_by(email=data["email"]).first():
            return {"message": "Email already registered"}, 409

        user = User(
            username=data["username"],
            email=data["email"],
            role=payload.get("role", "player"),
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        profile = Profile(user_id=user.id, full_name=payload.get("full_name", data["username"]))
        db.session.add(profile)
        db.session.commit()

        token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        return {"access_token": token, "user": user_schema.dump(user)}, 201


class LoginResource(Resource):
    def post(self):
        payload = request.get_json() or {}
        username = payload.get("username")
        password = payload.get("password")

        if not username or not password:
            return {"message": "username and password are required"}, 400

        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        if not user or not user.check_password(password):
            return {"message": "Invalid credentials"}, 401

        token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        return {"access_token": token, "user": user_schema.dump(user)}, 200


class MeResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(int(user_id))
        return user_schema.dump(user), 200

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(int(user_id))
        payload = request.get_json() or {}

        if not user.profile:
            user.profile = Profile(user_id=user.id)

        for field in ("full_name", "bio", "avatar_url", "phone", "country"):
            if field in payload:
                setattr(user.profile, field, payload[field])

        db.session.commit()
        return user_schema.dump(user), 200
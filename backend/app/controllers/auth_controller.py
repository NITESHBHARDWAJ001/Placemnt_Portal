from flask import request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from app.models import User
from app.schemas.auth_schema import LoginSchema, RegisterSchema, UserSchema
from app.services.auth_service import AuthService
from app.utils.api_response import success_response
from app.utils.exceptions import NotFoundError

register_schema = RegisterSchema()
login_schema = LoginSchema()
user_schema = UserSchema()


class AuthController:
    @staticmethod
    def register():
        data = register_schema.load(request.get_json(force=True))
        user = AuthService.register(data)
        return success_response("Registration successful. You can now log in.", user_schema.dump(user), status_code=201)

    @staticmethod
    def login():
        data = login_schema.load(request.get_json(force=True))
        user, access_token, refresh_token = AuthService.login(data["email"], data["password"])
        return success_response(
            "Login successful",
            {
                "user": user_schema.dump(user),
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
        )

    @staticmethod
    @jwt_required(refresh=True)
    def refresh():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user is None:
            raise NotFoundError("User not found")
        access_token = AuthService.refresh(user)
        return success_response("Token refreshed", {"access_token": access_token})

    @staticmethod
    @jwt_required()
    def me():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return success_response("Current user", user_schema.dump(user))

    @staticmethod
    @jwt_required()
    def logout():
        AuthService.logout()
        return success_response("Logged out successfully")

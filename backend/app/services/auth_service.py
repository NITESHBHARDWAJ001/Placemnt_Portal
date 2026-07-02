from datetime import datetime, timezone

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt

from app.extensions import db
from app.models import CompanyProfile, StudentProfile, TokenBlocklist
from app.repositories.user_repository import UserRepository
from app.services.activity_log_service import ActivityLogService
from app.utils.enums import CompanyApprovalStatus, RoleEnum
from app.utils.exceptions import ConflictError, ForbiddenError, UnauthorizedError, ValidationError
from app.utils.security import hash_password, verify_password


class AuthService:
    @staticmethod
    def register(data: dict):
        email = data["email"].strip().lower()
        role = data["role"]

        if role == RoleEnum.ADMIN.value:
            raise ValidationError("Admin accounts cannot be self-registered")

        if UserRepository.email_exists(email):
            raise ConflictError("An account with this email already exists")

        user = UserRepository.create(
            name=data["name"].strip(),
            email=email,
            password_hash=hash_password(data["password"]),
            role=RoleEnum(role),
            is_active=True,
            is_blacklisted=False,
        )

        if role == RoleEnum.STUDENT.value:
            profile = StudentProfile(user_id=user.id)
            db.session.add(profile)
        elif role == RoleEnum.COMPANY.value:
            profile = CompanyProfile(
                user_id=user.id,
                company_name=data.get("company_name") or user.name,
                approval_status=CompanyApprovalStatus.PENDING,
            )
            db.session.add(profile)

        db.session.commit()
        ActivityLogService.log(user.id, "USER_REGISTERED", "User", user.id, f"{role} account registered")
        return user

    @staticmethod
    def login(email: str, password: str):
        user = UserRepository.get_by_email(email.strip().lower())
        if user is None or not verify_password(user.password_hash, password):
            raise UnauthorizedError("Invalid email or password")

        if not user.is_active:
            raise ForbiddenError("Your account has been deactivated. Contact the administrator.")
        if user.is_blacklisted:
            raise ForbiddenError("Your account has been blacklisted. Contact the administrator.")

        user.last_login_at = datetime.now(timezone.utc)
        db.session.commit()

        access_token, refresh_token = AuthService._issue_tokens(user)
        ActivityLogService.log(user.id, "USER_LOGIN", "User", user.id, "User logged in")
        return user, access_token, refresh_token

    @staticmethod
    def _issue_tokens(user):
        claims = {"role": user.role.value, "name": user.name, "email": user.email}
        access_token = create_access_token(identity=str(user.id), additional_claims=claims)
        refresh_token = create_refresh_token(identity=str(user.id), additional_claims=claims)
        return access_token, refresh_token

    @staticmethod
    def refresh(user):
        claims = {"role": user.role.value, "name": user.name, "email": user.email}
        return create_access_token(identity=str(user.id), additional_claims=claims)

    @staticmethod
    def logout():
        jti = get_jwt()["jti"]
        token_type = get_jwt()["type"]
        user_id = get_jwt()["sub"]
        TokenBlocklist.query.session.add(
            TokenBlocklist(jti=jti, token_type=token_type, user_id=user_id)
        )
        db.session.commit()

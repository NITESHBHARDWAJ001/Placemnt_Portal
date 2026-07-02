from marshmallow import Schema, fields, validate

from app.utils.enums import RoleEnum


class RegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    role = fields.Str(
        required=True, validate=validate.OneOf([RoleEnum.STUDENT.value, RoleEnum.COMPANY.value])
    )
    # optional company-specific field at registration time
    company_name = fields.Str(required=False, allow_none=True)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class RefreshResponseSchema(Schema):
    access_token = fields.Str()


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Email()
    role = fields.Method("get_role")
    is_active = fields.Bool()
    is_blacklisted = fields.Bool()
    created_at = fields.DateTime()
    last_login_at = fields.DateTime()

    def get_role(self, obj):
        return obj.role.value if hasattr(obj.role, "value") else obj.role

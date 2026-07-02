from marshmallow import Schema, fields, validate


class CompanyProfileUpdateSchema(Schema):
    company_name = fields.Str(required=False, allow_none=True, validate=validate.Length(max=150))
    website = fields.Str(required=False, allow_none=True)
    industry = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    logo_url = fields.Str(required=False, allow_none=True)
    hr_name = fields.Str(required=False, allow_none=True)
    hr_designation = fields.Str(required=False, allow_none=True)


class CompanyProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    email = fields.Method("get_email")
    is_active = fields.Method("get_is_active")
    is_blacklisted = fields.Method("get_is_blacklisted")
    company_name = fields.Str()
    website = fields.Str()
    industry = fields.Str()
    description = fields.Str()
    logo_url = fields.Str()
    hr_name = fields.Str()
    hr_designation = fields.Str()
    approval_status = fields.Method("get_status")
    approved_at = fields.DateTime()
    created_at = fields.DateTime()

    def get_email(self, obj):
        return obj.user.email if obj.user else None

    def get_is_active(self, obj):
        return obj.user.is_active if obj.user else None

    def get_is_blacklisted(self, obj):
        return obj.user.is_blacklisted if obj.user else None

    def get_status(self, obj):
        return obj.approval_status.value if hasattr(obj.approval_status, "value") else obj.approval_status

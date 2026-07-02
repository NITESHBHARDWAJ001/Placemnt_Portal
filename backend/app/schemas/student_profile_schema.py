from marshmallow import Schema, fields, validate

from app.schemas.resume_schema import ResumeSchema


class StudentProfileUpdateSchema(Schema):
    phone = fields.Str(required=False, allow_none=True, validate=validate.Length(max=20))
    dob = fields.Date(required=False, allow_none=True)
    gender = fields.Str(required=False, allow_none=True)
    address = fields.Str(required=False, allow_none=True, validate=validate.Length(max=255))
    degree = fields.Str(required=False, allow_none=True)
    branch = fields.Str(required=False, allow_none=True)
    batch_year = fields.Int(required=False, allow_none=True)
    cgpa = fields.Float(required=False, allow_none=True, validate=validate.Range(min=0, max=10))
    backlog_count = fields.Int(required=False, allow_none=True, validate=validate.Range(min=0))
    linkedin_url = fields.Str(required=False, allow_none=True)
    github_url = fields.Str(required=False, allow_none=True)
    portfolio_url = fields.Str(required=False, allow_none=True)


class SkillSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class StudentProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    name = fields.Method("get_name")
    email = fields.Method("get_email")
    is_active = fields.Method("get_is_active")
    is_blacklisted = fields.Method("get_is_blacklisted")
    phone = fields.Str()
    dob = fields.Date()
    gender = fields.Str()
    address = fields.Str()
    degree = fields.Str()
    branch = fields.Str()
    batch_year = fields.Int()
    cgpa = fields.Float()
    backlog_count = fields.Int()
    linkedin_url = fields.Str()
    github_url = fields.Str()
    portfolio_url = fields.Str()
    placement_status = fields.Method("get_placement_status")
    profile_completion_percent = fields.Int()
    skills = fields.Method("get_skills")
    resumes = fields.List(fields.Nested(ResumeSchema), attribute="resumes")

    def get_name(self, obj):
        return obj.user.name if obj.user else None

    def get_email(self, obj):
        return obj.user.email if obj.user else None

    def get_is_active(self, obj):
        return obj.user.is_active if obj.user else None

    def get_is_blacklisted(self, obj):
        return obj.user.is_blacklisted if obj.user else None

    def get_placement_status(self, obj):
        return obj.placement_status.value if hasattr(obj.placement_status, "value") else obj.placement_status

    def get_skills(self, obj):
        return [ss.skill.name for ss in obj.skills]

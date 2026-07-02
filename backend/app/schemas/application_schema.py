from marshmallow import Schema, fields, validate

from app.schemas.interview_schema import InterviewSchema
from app.utils.enums import ApplicationStatus


class ApplicationCreateSchema(Schema):
    resume_id = fields.Int(required=False, allow_none=True)


class ApplicationStatusUpdateSchema(Schema):
    status = fields.Str(required=True, validate=validate.OneOf([s.value for s in ApplicationStatus]))


class ApplicationSchema(Schema):
    id = fields.Int(dump_only=True)
    student_profile_id = fields.Int()
    student_name = fields.Method("get_student_name")
    student_email = fields.Method("get_student_email")
    student_cgpa = fields.Method("get_student_cgpa")
    student_branch = fields.Method("get_student_branch")
    drive_id = fields.Int()
    drive_title = fields.Method("get_drive_title")
    company_name = fields.Method("get_company_name")
    resume_id = fields.Int()
    status = fields.Method("get_status")
    applied_at = fields.DateTime()
    interviews = fields.List(fields.Nested(InterviewSchema))

    def get_student_name(self, obj):
        return obj.student_profile.user.name if obj.student_profile and obj.student_profile.user else None

    def get_student_email(self, obj):
        return obj.student_profile.user.email if obj.student_profile and obj.student_profile.user else None

    def get_student_cgpa(self, obj):
        return obj.student_profile.cgpa if obj.student_profile else None

    def get_student_branch(self, obj):
        return obj.student_profile.branch if obj.student_profile else None

    def get_drive_title(self, obj):
        return obj.drive.title if obj.drive else None

    def get_company_name(self, obj):
        return obj.drive.company_profile.company_name if obj.drive and obj.drive.company_profile else None

    def get_status(self, obj):
        return obj.status.value if hasattr(obj.status, "value") else obj.status

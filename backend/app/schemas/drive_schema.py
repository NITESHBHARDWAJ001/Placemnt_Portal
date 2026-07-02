from marshmallow import Schema, fields, validate

from app.utils.enums import DriveStatus, JobType


class DriveCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=3, max=150))
    description = fields.Str(required=False, allow_none=True)
    job_role = fields.Str(required=False, allow_none=True)
    job_type = fields.Str(
        load_default=JobType.FULL_TIME.value,
        validate=validate.OneOf([j.value for j in JobType]),
    )
    package_min = fields.Float(required=False, allow_none=True)
    package_max = fields.Float(required=False, allow_none=True)
    location = fields.Str(required=False, allow_none=True)
    min_cgpa = fields.Float(load_default=0, validate=validate.Range(min=0, max=10))
    max_backlogs = fields.Int(load_default=0, validate=validate.Range(min=0))
    allowed_branches = fields.List(fields.Str(), required=False, load_default=list)
    eligible_batch = fields.Int(required=False, allow_none=True)
    application_deadline = fields.DateTime(required=True)
    drive_date = fields.DateTime(required=False, allow_none=True)


class DriveUpdateSchema(DriveCreateSchema):
    title = fields.Str(required=False, validate=validate.Length(min=3, max=150))
    application_deadline = fields.DateTime(required=False)


class DriveSchema(Schema):
    id = fields.Int(dump_only=True)
    company_profile_id = fields.Int()
    company_name = fields.Method("get_company_name")
    title = fields.Str()
    description = fields.Str()
    job_role = fields.Str()
    job_type = fields.Method("get_job_type")
    package_min = fields.Float()
    package_max = fields.Float()
    location = fields.Str()
    min_cgpa = fields.Float()
    max_backlogs = fields.Int()
    allowed_branches = fields.Method("get_branches")
    eligible_batch = fields.Int()
    application_deadline = fields.DateTime()
    drive_date = fields.DateTime()
    status = fields.Method("get_status")
    applicant_count = fields.Method("get_applicant_count")
    created_at = fields.DateTime()

    def get_company_name(self, obj):
        return obj.company_profile.company_name if obj.company_profile else None

    def get_job_type(self, obj):
        return obj.job_type.value if hasattr(obj.job_type, "value") else obj.job_type

    def get_status(self, obj):
        return obj.status.value if hasattr(obj.status, "value") else obj.status

    def get_branches(self, obj):
        return obj.branches_list()

    def get_applicant_count(self, obj):
        return len(obj.applications) if obj.applications is not None else 0

from marshmallow import Schema, fields, validate

from app.utils.enums import InterviewMode, InterviewResult, InterviewStatus


class InterviewCreateSchema(Schema):
    round_number = fields.Int(load_default=1, validate=validate.Range(min=1))
    round_name = fields.Str(required=False, allow_none=True)
    scheduled_at = fields.DateTime(required=True)
    mode = fields.Str(
        load_default=InterviewMode.ONLINE.value, validate=validate.OneOf([m.value for m in InterviewMode])
    )
    location_or_link = fields.Str(required=False, allow_none=True)
    interviewer_name = fields.Str(required=False, allow_none=True)


class InterviewUpdateSchema(Schema):
    status = fields.Str(required=False, validate=validate.OneOf([s.value for s in InterviewStatus]))
    result = fields.Str(required=False, validate=validate.OneOf([r.value for r in InterviewResult]))
    feedback = fields.Str(required=False, allow_none=True)
    scheduled_at = fields.DateTime(required=False)


class InterviewSchema(Schema):
    id = fields.Int(dump_only=True)
    application_id = fields.Int()
    round_number = fields.Int()
    round_name = fields.Str()
    scheduled_at = fields.DateTime()
    mode = fields.Method("get_mode")
    location_or_link = fields.Str()
    interviewer_name = fields.Str()
    status = fields.Method("get_status")
    result = fields.Method("get_result")
    feedback = fields.Str()

    def get_mode(self, obj):
        return obj.mode.value if hasattr(obj.mode, "value") else obj.mode

    def get_status(self, obj):
        return obj.status.value if hasattr(obj.status, "value") else obj.status

    def get_result(self, obj):
        return obj.result.value if hasattr(obj.result, "value") else obj.result

from marshmallow import Schema, fields, validate


class BlacklistCreateSchema(Schema):
    reason = fields.Str(required=True, validate=validate.Length(min=3, max=500))


class BlacklistLogSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    reason = fields.Str()
    is_active = fields.Bool()
    blacklisted_at = fields.DateTime()
    revoked_at = fields.DateTime()

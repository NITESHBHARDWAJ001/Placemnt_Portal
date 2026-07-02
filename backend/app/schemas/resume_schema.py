from marshmallow import Schema, fields


class ResumeSchema(Schema):
    id = fields.Int(dump_only=True)
    file_name = fields.Str()
    is_active = fields.Bool()
    created_at = fields.DateTime()

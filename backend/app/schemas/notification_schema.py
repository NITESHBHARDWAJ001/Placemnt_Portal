from marshmallow import Schema, fields


class NotificationSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    message = fields.Str()
    type = fields.Method("get_type")
    link = fields.Str()
    is_read = fields.Bool()
    created_at = fields.DateTime()

    def get_type(self, obj):
        return obj.type.value if hasattr(obj.type, "value") else obj.type

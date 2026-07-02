from marshmallow import Schema, fields


class ActivityLogSchema(Schema):
    id = fields.Int(dump_only=True)
    actor_name = fields.Method("get_actor_name")
    action = fields.Str()
    entity_type = fields.Str()
    entity_id = fields.Int()
    description = fields.Str()
    created_at = fields.DateTime()

    def get_actor_name(self, obj):
        return obj.actor.name if obj.actor else "System"

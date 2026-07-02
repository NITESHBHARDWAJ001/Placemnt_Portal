from marshmallow import Schema, fields, validate


class PaginationQuerySchema(Schema):
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=10, validate=validate.Range(min=1, max=100))
    search = fields.Str(load_default=None, allow_none=True)
    sort_by = fields.Str(load_default=None, allow_none=True)
    order = fields.Str(load_default="desc", validate=validate.OneOf(["asc", "desc"]))

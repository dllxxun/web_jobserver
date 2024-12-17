from marshmallow import Schema, fields

class JobSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    company = fields.Str(required=True)
    location = fields.Str(required=True)
    salary_range = fields.Str()
    requirements = fields.List(fields.Str())
    category = fields.Str()
    job_type = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

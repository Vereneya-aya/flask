from marshmallow import Schema, fields

class BookSchema(Schema):
    title = fields.String(required=True)
    author = fields.String(required=True)
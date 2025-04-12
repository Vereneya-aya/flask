# schemas.py
from marshmallow import Schema, fields

class BookSchema(Schema):
    id = fields.Int(dump_only=True)  # Автоматически создается, не нужно передавать
    title = fields.Str(required=True)
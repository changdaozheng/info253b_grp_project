from marshmallow import Schema, fields

class PetsSchema(Schema):
    """Marshmallow schema for pets"""
    id = fields.UUID(dump_only=True)
    user_id = fields.UUID()
    name = fields.String()
    breed = fields.String()
    
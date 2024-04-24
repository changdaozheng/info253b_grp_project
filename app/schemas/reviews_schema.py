from marshmallow import Schema, fields

class ReviewsSchema(Schema):
    """Marshmallow schema for reviews"""
    id = fields.UUID(dump_only=True)
    places_id = fields.UUID()
    user_id = fields.UUID()
    pet_id = fields.UUID()
    score = fields.Float()
    content = fields.String()
    